#!/usr/bin/env python3
"""Daily official Work24 open-recruitment discovery. Requires WORK24_API_KEY.
Uses public recruitment list endpoint and preserves previous discoveries.
No scraping of Jasoseol or inference of qualifications/pay.
"""
import datetime as dt
import html
import json
import os
from pathlib import Path
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'auto_jobs.json'
URL = 'https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo210L21.do'
KST = dt.timezone(dt.timedelta(hours=9))
TODAY = dt.datetime.now(KST).date()
TRACKS = [
    (1, ('소재', '화학', '고분자', '재료', '전해질', '슬러리', '배터리', '이차전지', '전지', '촉매', '코팅', '표면처리', '도금', '연구개발', 'r&d')),
    (2, ('생산기술', '공정기술', '공정개발', '양산기술', '공정엔지니어', '생산공정', '제조기술', '반도체', '품질기술', 'process engineer')),
    (3, ('데이터분석', '데이터 분석', '스마트팩토리', '스마트공장', '제조데이터', '제조 데이터', 'dx', 'ax', '데이터사이언', '머신러닝', 'ai 엔지니어')),
    (4, ('esg', '탄소중립', '온실가스', '환경데이터', '환경 데이터', '탄소배출', '환경관리', '환경경영', '환경안전')),
]
BLOCK = ('영업', '마케팅', '회계', '재무', '인사', '총무', '구매', '경영지원', '법무', '디자인', '서비스직', '상담', '콜센터', '채용연계형', '인턴십', '영업관리')


def simple(el, name):
    v = el.findtext(name, default='')
    return (v or '').strip()


def date_string(x):
    x = re.sub(r'\D', '', x)
    if len(x) >= 8:
        try:
            return dt.date(int(x[:4]), int(x[4:6]), int(x[6:8])).isoformat()
        except ValueError:
            pass
    return ''


def safe(x):
    return html.escape(x.strip(), quote=True)[:350]


def download(page):
    query = {'authKey': os.environ['WORK24_API_KEY'], 'callTp': 'L', 'returnType': 'XML', 'startPage': page, 'display': 100,
             'coClcd': '10|40', 'empWantedTypeCd': '10', 'sortField': 'regDt', 'sortOrderBy': 'desc'}
    req = urllib.request.Request(URL + '?' + urllib.parse.urlencode(query), headers={'User-Agent':'SabinCareerRadar/1.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        payload = r.read(5_000_000)
    root = ET.fromstring(payload)
    entries = root.findall('.//dhsOpenEmpInfo')
    if not entries and page == 1:
        raise RuntimeError('고용24 API가 공고 목록을 반환하지 않았습니다. 키/접근권한/응답 형식을 확인하세요.')
    return entries


def classify(title):
    lowered = title.lower()
    if any(w in lowered for w in BLOCK):
        return None
    matched = [(cat, sum(word in lowered for word in words)) for cat, words in TRACKS]
    matched = [(cat, count) for cat, count in matched if count]
    if not matched: return None
    return max(matched, key=lambda t: t[1])[0]


def convert(el):
    title = simple(el, 'empWantedTitle')
    company = simple(el, 'empBusiNm')
    seq = simple(el, 'empSeqno')
    start = date_string(simple(el, 'empWantedStdt'))
    end = date_string(simple(el, 'empWantedEndt'))
    link = simple(el, 'empWantedHomepgDetail') or simple(el, 'empWantedMobileUrl')
    cat = classify(title)
    if not seq or not title or not company or not start or not end or not cat:
        return None
    if end < TODAY.isoformat():
        return None
    u = urllib.parse.urlparse(link)
    if u.scheme != 'https' and u.scheme != 'http':
        return None
    if not u.netloc:
        return None
    kind = simple(el, 'empWantedTypeNm') or '정규직'
    return {
        'id':'auto-work24-'+re.sub(r'[^A-Za-z0-9_-]','',seq),
        'company':safe(company), 'title':safe(title), 'start':start,'end':end,
        'cat':cat,'score':None,'loc':'공고에서 확인','kind':safe(kind),
        'roles':safe(title),'fit':'공고 제목이 관심 직무 키워드와 일치합니다. 세부 지원 자격은 원문에서 확인하세요.',
        'url':link, 'source':'고용24 공채속보', 'auto':True,
        'qual':'직무별 지원 자격은 공고 원문 확인', 'requiredYears':'미확인',
        'process':'원문에서 확인', 'firstSeen':TODAY.isoformat()
    }


def main():
    if not os.getenv('WORK24_API_KEY'):
        print('WORK24_API_KEY 미설정 — 기존 데이터 유지, 자동 수집은 실행하지 않음')
        return 0
    old = {'lastChecked':None,'records':[]}
    if DATA.exists():
        old = json.loads(DATA.read_text(encoding='utf-8'))
    by_id = {r['id']:r for r in old.get('records', [])}
    found = 0
    for p in range(1, 5):
        entries = download(p)
        for e in entries:
            r = convert(e)
            if not r: continue
            found += 1
            if r['id'] in by_id:
                r['firstSeen'] = by_id[r['id']].get('firstSeen',r['firstSeen'])
            by_id[r['id']] = r
        if len(entries) < 100:
            break
    # Archive remains limited to last 365 days; expired recent records are kept for historical comparison.
    cutoff = TODAY - dt.timedelta(days=365)
    kept = []
    for v in by_id.values():
        try:
            if dt.date.fromisoformat(v['end']) >= cutoff:
                kept.append(v)
        except (ValueError,KeyError):
            pass
    kept.sort(key=lambda x:(x['start'],x['id']),reverse=True)
    output = {'lastChecked':TODAY.isoformat(), 'source':'고용24 공채속보 OPEN API', 'records':kept[:500]}
    DATA.parent.mkdir(parents=True,exist_ok=True)
    DATA.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'자동 수집 완료: 이번 검색 {found}건, 누적 보관 {len(output["records"])}건')
    return 0

if __name__ == '__main__':
    try: sys.exit(main())
    except Exception as exc:
        print(f'자동 수집 실패 (기존 파일 보존): {exc}',file=sys.stderr)
        sys.exit(1)
