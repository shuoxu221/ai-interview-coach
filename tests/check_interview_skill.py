from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ai-interview-coach"
PROMPT = ROOT / "prompts" / "AI模拟面试-普通AI复制版.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class InterviewSkillContract(unittest.TestCase):
    def test_requires_jd_resume_and_mode_before_starting(self):
        text = read(SKILL / "SKILL.md") + read(SKILL / "references/interview-workflow.md")
        for token in ("target JD", "redacted resume", "训练模式", "实战模式", "开始面试"):
            self.assertIn(token, text)

    def test_training_mode_has_bounded_follow_up_scoring_and_retry(self):
        text = read(SKILL / "references/interview-workflow.md") + read(SKILL / "references/debrief-template.md")
        for token in ("最多连续追问 3 轮", "内容与证据", "逻辑结构", "岗位匹配", "表达清晰", "重答本题"):
            self.assertIn(token, text)

    def test_realistic_mode_withholds_mid_session_coaching(self):
        text = read(SKILL / "references/interview-workflow.md")
        self.assertIn("中途禁止提示、评分、表扬、纠错、示范答案和框架名称", text)
        self.assertIn("统一输出复盘", text)

    def test_fact_semantics_and_conflicts_are_protected(self):
        text = read(SKILL / "SKILL.md") + read(SKILL / "references/follow-up-rules.md")
        for token in ("提升至22%", "提升了22%", "约30天", "团队", "事实口径待确认"):
            self.assertIn(token, text)

    def test_sensitive_questions_and_hiring_guarantees_are_forbidden(self):
        text = read(SKILL / "SKILL.md")
        for token in ("marriage", "fertility", "disease", "religion", "Never promise"):
            self.assertIn(token, text)

    def test_copy_prompt_preserves_dual_mode_contract(self):
        text = read(PROMPT)
        for token in (
            "【岗位JD】",
            "【脱敏简历】",
            "【模式】",
            "训练模式",
            "实战模式",
            "一次只问一个问题",
            "最多连续追问3轮",
            "提升至22%",
            "结束面试",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
