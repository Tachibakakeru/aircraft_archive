"""Register the original Blender prototype without overwriting existing descriptions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    path=ROOT/'data/concorde.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    data['parts']['nose'] = {
        'name': {'zh':'可下垂機鼻','en':'Droop nose','ja':'可動機首'},
        'en':'DROOP NOSE',
        'summary': {
            'zh':'協和號機鼻可設定為 0°、5° 與 12.5°，讓起降高迎角時仍可看見跑道。本頁可動部位滑桿示範 0–12.5° 下垂；六片襟副翼、雙段方向舵與三組起落架也可分別操作。',
            'en':'Concorde used nose settings of 0°, 5° and 12.5° for visibility at high angles of attack. The moving-parts sliders demonstrate nose droop, six elevons, split rudders and three landing-gear assemblies.',
            'ja':'機首は0°、5°、12.5°に設定でき、高迎角での滑走路視認性を確保します。可動部位スライダーで機首、6枚のエレボン、上下ラダー、3組の脚を操作できます。'},
        'fact': {
            'zh':'此為 Blender 原創教學試作模型。護罩目前隨機鼻移動，尚未重現獨立滑入機鼻的機構；主架先縮短再向內收，鼻架向後收，仍未模擬艙門與完整多連桿。襟副翼位於引擎短艙內外側，操控時引擎保持固定。',
            'en':'Original Blender educational prototype. The visor follows the nose; independent visor sliding is not reproduced. Main legs shorten before retracting inward, while the nose gear retracts aft; doors and full linkages remain simplified. Elevons lie inboard and outboard of the nacelles; engines stay fixed.',
            'ja':'Blenderオリジナル教育用試作です。バイザーは機首と共に動き、独立収納は未再現です。主脚は短縮して内側へ、前脚は後方へ格納しますが、扉と完全なリンク機構は未再現です。エレボンはナセルの内外側にあり、エンジンは固定です。'},
        'bullets': [], 'specs': [], 'images': []}
    if 'nose' not in data['partOrder']:
        data['partOrder'].insert(data['partOrder'].index('cockpit')+1,'nose')
    for url in ['https://www.heritageconcorde.com/nose-and-visor-operations','https://www.heritageconcorde.com/concorde-elevons-and-rudder','https://www.britishairways.com/content/information/about-ba/history-and-heritage/celebrating-concorde']:
        if url not in data['sources']: data['sources'].append(url)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'data/fleet.json'
    fleet=json.loads(path.read_text(encoding='utf-8'))
    target=next(a for a in fleet['aircraft'] if a['id']=='concorde')
    target['has3d']=True
    target['thumb']='assets/thumb_concorde.png?v=182'
    path.write_text(json.dumps(fleet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
