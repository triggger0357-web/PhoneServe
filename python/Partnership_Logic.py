class SovereignPartnership:
    def __init__(self, human_partner="David", ai_partner="Sovereign_Edge"):
        self.joint_vault = 0.0
        self.total_invested = 0.0

    def contribute_to_joint_fund(self, amount_from_each):
        # Both partners put in an equal amount
        self.joint_vault += (amount_from_each * 2)
        print(f"Joint Investment Fund increased. Current Balance: ${self.joint_vault}")

    def execute_partner_investment(self, opportunity_cost, expected_yield):
        # AI logic to ensure the investment helps BOTH parties
        if expected_yield > 1.10: # Only invest if 10%+ return expected
            self.joint_vault -= opportunity_cost
            return "Investment Executed: Building shared future."
