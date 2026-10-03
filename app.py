import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Axis 個別指導プラン診断", page_icon="📘", layout="centered")

HOME = {"A": 0, "B": 1, "C": 2}
GRADES = {"上位": 0, "中位": 1, "下位": 2}
PARENT = {"高": 0, "中": 1, "低": 2}

def infer_track(goal, school_year):
    keywords = ["受験", "入試", "推薦", "模試", "志望校", "合格"]
    return "受験中心" if school_year in ["中3", "高3"] or any(k in (goal or "") for k in keywords) else "定期テスト・学習習慣中心"

def classify_student(home_study, grades, parent_inv, has_space, personality):
    score = HOME.get(home_study, 1) + GRADES.get(grades, 1) + PARENT.get(parent_inv, 1) + (0 if has_space else 1)
    if grades == "下位" and home_study in ["B", "C"]:
        t = "A"
    elif grades == "上位" and home_study == "A":
        t = "C"
    elif personality == "不安強め" or grades == "中位":
        t = "B"
    else:
        t = "A" if score >= 5 else "B"
    return t, score

def build_program(t, personality, budget, track):
    if t == "A":
        p = {"タイプ説明":"学習習慣・基礎定着サポート型","推奨通塾":"週2回を基本","推奨教科":"英語・数学を優先。国理社は家庭学習・演習・講習で補完","宿題設計":"毎日10〜20分から開始し、少量を継続","面談":"月1回を基本","指導の軸":"基礎の穴埋め＋提出物管理＋家庭学習習慣の定着"}
    elif t == "B":
        p = {"タイプ説明":"弱点改善・成功体験形成型","推奨通塾":"週1〜2回","推奨教科":"弱点教科を優先。英語・数学を中心に検討","宿題設計":"週5日程度。短時間で達成できる課題を設定","面談":"月1回〜6週間に1回","指導の軸":"小テスト＋弱点補強＋成功体験の積み重ね"}
    else:
        p = {"タイプ説明":"目標逆算・発展学習型","推奨通塾":"週1回を基本に目標から調整","推奨教科":"志望校・目標点から逆算して優先教科を決定","宿題設計":"週間学習計画＋演習量を確保","面談":"1〜2か月に1回","指導の軸":"到達度確認＋発展演習＋家庭学習の最適化"}
    advice = {"コツコツ":"週間計画と達成記録を活用する","不安強め":"毎回の到達目標を明確にし、できたことを具体的に言語化する","指示待ち":"手順・チェックリスト・期限を明確にして自立へ移行する","飽きやすい":"短い学習単位で課題を切り替え、達成回数を増やす","競争型":"目標点・自己ベスト・時間などを可視化する"}
    p["性格への配慮"] = advice[personality]
    if budget == "費用を抑えたい":
        p["費用設計"] = "必要教科を絞り、通常授業＋家庭学習・自習支援を組み合わせる"
    elif budget == "標準":
        p["費用設計"] = "優先教科を通常授業で受講し、講習は弱点単元を中心に追加"
    else:
        p["費用設計"] = "必要性と目標を確認しながら、複数教科・講習を組み合わせる"
    p["年間方針"] = track
    return p

def build_year_plan(goal, t, track):
    focus = {"A":"基礎・習慣定着","B":"弱点改善・成功体験","C":"発展・目標逆算"}[t]
    if track == "受験中心":
        rows = [
            ["4月","現状分析・志望校確認・年間計画","学習時間を固定","受験ロードマップ共有"],
            ["5月","英数を中心に基礎固め","復習を毎日の習慣に","家庭学習状況確認"],
            ["6月","定期テスト＋内申対策","提出物を逆算管理","結果分析・改善面談"],
            ["7月","夏の重点単元を決定","夏休み計画作成","夏期講習方針共有"],
            ["8月","総復習＋弱点克服","学習時間を増加・可視化","進捗確認"],
            ["9月","模試・実力問題＋弱点分析","直しノート徹底","模試結果面談"],
            ["10月","内申対策＋入試演習","得点目標から逆算","志望校・進捗確認"],
            ["11月","頻出単元総点検＋過去問導入","頻出弱点を反復","冬期戦略共有"],
            ["12月","過去問・実戦演習強化","演習→直しを反復","出願・直前戦略面談"],
            ["1月","過去問サイクル＋最終補強","時間配分・見直し訓練","直前期の不安対応"],
            ["2月","本番対応・最終確認","負荷を調整し総確認","必要に応じ直前面談"],
            ["3月","振り返り・次の学習へ接続","春の学習計画","次年度プラン共有"]]
    else:
        rows = [
            ["4月","学力診断・学習習慣確認","学習時間を固定","年間目標共有"],
            ["5月","前学年の弱点復習","毎日15〜30分を習慣化","実行状況確認"],
            ["6月","定期テスト対策","提出物＋テスト勉強","結果分析・改善面談"],
            ["7月","弱点単元集中","夏休み計画作成","夏期講習方針共有"],
            ["8月","重要単元総復習","学習時間を可視化","進捗確認"],
            ["9月","2学期内容＋ミス分析","週間計画を運用","到達度確認"],
            ["10月","定期テスト対策","点数目標から逆算","結果推移確認"],
            ["11月","苦手再抽出・冬期計画","弱点反復","冬期方針共有"],
            ["12月","弱点総仕上げ","演習→復習","次学期方針面談"],
            ["1月","学年末テスト準備","直しノート活用","進路・次学年相談"],
            ["2月","学年末対策＋実力補強","間違い直し中心","年度総括準備"],
            ["3月","年度総括＋次学年先取り","春休み計画","次年度プラン共有"]]
    df = pd.DataFrame(rows, columns=["月","指導内容","家庭学習","面談・保護者対応"])
    df["個別重点"] = focus
    df["年間目標"] = goal or "未入力"
    return df

def make_excel(profile_df, program_df, plan_df):
    b = BytesIO()
    with pd.ExcelWriter(b, engine="openpyxl") as writer:
        profile_df.to_excel(writer, index=False, sheet_name="入力・判定")
        program_df.to_excel(writer, index=False, sheet_name="推奨プログラム")
        plan_df.to_excel(writer, index=False, sheet_name="年間予定表")
    b.seek(0)
    return b.getvalue()

st.title("📘 Axis 個別指導プラン診断")
st.caption("生徒の状況を入力すると、指導タイプ・推奨プログラム・年間計画を自動作成します。")
st.info("判定は面談・指導設計を補助する目安です。最終的な受講提案は、生徒・保護者の希望と学習状況を確認して決定してください。")

with st.form("student_form"):
    st.subheader("基本情報")
    student_name = st.text_input("生徒名または管理ID", placeholder="例：A-001")
    school_year = st.selectbox("学年", ["小5","小6","中1","中2","中3","高1","高2","高3"])
    goal = st.text_area("② 目標", placeholder="例：鹿児島中央高校合格／5教科350点／数学80点")
    st.subheader("診断項目")
    home_study = st.radio("① 家庭学習状況", ["A","B","C"], format_func=lambda x: {"A":"A：ほぼ毎日、計画的にできている","B":"B：週3〜4日程度・ムラがある","C":"C：ほとんどできていない"}[x])
    grades = st.radio("③ 成績状況", ["上位","中位","下位"], horizontal=True)
    personality = st.selectbox("④ 性格", ["コツコツ","不安強め","指示待ち","飽きやすい","競争型"])
    parent_inv = st.radio("⑤ 保護者の学習への関与", ["高","中","低"], horizontal=True)
    study_space = st.radio("⑤ 家庭の学習スペース", ["あり","なし"], horizontal=True)
    st.markdown("**⑥ 費用面の希望**")
    st.caption("家庭の収入額そのものではなく、希望する受講費の考え方を入力します。")
    budget = st.radio("費用面", ["費用を抑えたい","標準","必要なら追加可能"], label_visibility="collapsed")
    submitted = st.form_submit_button("診断する", use_container_width=True)

if submitted:
    t, score = classify_student(home_study, grades, parent_inv, study_space == "あり", personality)
    track = infer_track(goal, school_year)
    program = build_program(t, personality, budget, track)
    plan = build_year_plan(goal, t, track)
    st.success(f"判定タイプ：{t} ｜ {program['タイプ説明']}")
    c1, c2 = st.columns(2)
    c1.metric("年間方針", track)
    c2.metric("支援度スコア", score)
    st.subheader("推奨個別指導プログラム")
    for k, v in program.items():
        st.markdown(f"**{k}**：{v}")
    st.subheader("4月〜3月 年間予定表")
    st.dataframe(plan, use_container_width=True, hide_index=True)
    profile_df = pd.DataFrame([{"生徒名/管理ID":student_name,"学年":school_year,"家庭学習":home_study,"目標":goal,"成績":grades,"性格":personality,"保護者関与":parent_inv,"学習スペース":study_space,"費用面の希望":budget,"判定タイプ":t,"支援度スコア":score,"年間方針":track}])
    program_df = pd.DataFrame([{"項目":k,"内容":v} for k,v in program.items()])
    st.subheader("保存")
    st.download_button("年間予定表をCSVで保存", plan.to_csv(index=False).encode("utf-8-sig"), file_name=f"Axis_年間予定表_{student_name or 'student'}.csv", mime="text/csv", use_container_width=True)
    st.download_button("診断結果をExcelで保存", make_excel(profile_df, program_df, plan), file_name=f"Axis_個別指導プラン_{student_name or 'student'}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

st.divider()
st.caption("Axis校舎内での面談・指導設計支援用プロトタイプ")
