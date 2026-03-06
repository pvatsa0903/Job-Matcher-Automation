import unittest

from job_matcher.scoring import score_job, score_text


class ScoringTests(unittest.TestCase):
    def test_weighted_resume_signals_score_higher(self) -> None:
        high_signal = {
            "title": "Senior Product Manager, Growth and Monetization",
            "description": (
                "Drive retention and lifecycle CRM strategy, run A/B testing, "
                "and optimize B2C SaaS subscriptions at 35 million user scale."
            ),
            "tags": ["incentives", "gamification"],
        }
        low_signal = {
            "title": "Product Manager",
            "description": "Lead roadmap execution and cross-functional delivery.",
        }
        high = score_job(high_signal)
        low = score_job(low_signal)

        self.assertGreater(high.total_score, low.total_score)
        self.assertGreaterEqual(high.total_score, 15.0)
        self.assertEqual(low.total_score, 0.0)

    def test_scale_signal_matches_30m_plus_language(self) -> None:
        scored = score_text("You will own systems that serve 30 million monthly users.")
        signals = {s.signal for s in scored.matched_signals}
        self.assertIn("scale_30m_plus", signals)

    def test_lifecycle_and_crm_are_detected(self) -> None:
        scored = score_text("Own lifecycle marketing and CRM programs across channels.")
        signals = {s.signal for s in scored.matched_signals}
        self.assertIn("lifecycle_crm", signals)

    def test_experimentation_detects_ab_testing(self) -> None:
        scored = score_text("Lead experimentation strategy with A/B testing and analysis.")
        signals = {s.signal for s in scored.matched_signals}
        self.assertIn("experimentation", signals)

    def test_saas_and_b2b_b2c_signal_is_detected(self) -> None:
        scored = score_text("Experience across B2B and B2C SaaS products is required.")
        signals = {s.signal for s in scored.matched_signals}
        self.assertIn("b2b_b2c_saas", signals)

    def test_incentive_and_gamification_signals_are_detected(self) -> None:
        scored = score_text("Build incentives with points and badges to deepen engagement.")
        signals = {s.signal for s in scored.matched_signals}
        self.assertIn("incentives", signals)
        self.assertIn("gamification", signals)

    def test_unrelated_text_scores_zero(self) -> None:
        scored = score_text("Maintain CI pipelines and improve internal tooling reliability.")
        self.assertEqual(scored.total_score, 0.0)
        self.assertEqual(len(scored.matched_signals), 0)


if __name__ == "__main__":
    unittest.main()
