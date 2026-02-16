import os
import asyncio
from pydantic import BaseModel
from agents import Agent, ModelSettings, RunContextWrapper, Runner, trace
from agents.tool import function_tool
from auto_mode import input_with_fallback, confirm_with_fallback
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# load into memory
load_dotenv(find_dotenv())

API_KEY = os.getenv('OAI_API_KEY')

client = OpenAI(api_key=API_KEY)

"""
Autonomous Anti-Money Laundering / Fraud investigation demo.
Simulates how an AI agent could investigate a suspicious transaction
by pulling data from multiple systems and escalting if needed. 

Follows an example from the OAI docs: 
https://github.com/openai/openai-agents-python/blob/main/examples/agent_patterns/agents_as_tools_conditional.py#L125
"""

import asyncio
from pydantic import BaseModel
from agents import Agent, ModelSettings, RunContextWrapper, Runner, trace
from agents.tool import function_tool
from examples.auto_mode import confirm_with_fallback, input_with_fallback

"""
Autonomous AML Investigation Agent
Realistic version: ML systems detect risk, agent performs investigation.
"""


# ---- Context ----

class InvestigationContext(BaseModel):
    transaction_id: str
    escalation_threshold: float = 0.75


# ---- Detection & Intelligence Tools ----

@function_tool
async def internal_fraud_model(transaction_id: str) -> str:
    return (
        "Internal model risk score: 0.82. "
        "Reasons: new beneficiery, amount anomaly, device mismatch."
    )


@function_tool
async def vendor_fraud_platform(transaction_id: str) -> str:
    return (
        "Vendor platform (e.g. Feedzai) score: 0.79. "
        "Pattern similar to known mule networks."
    )


@function_tool
async def data_fusion_cross_bank(transaction_id: str) -> str:
    return (
        "Data Fusion insight: Beneficiary account appears in two other banks."
        "Linked to accounts involved in account segregation patterns."
    )


@function_tool
async def customer_behavior_profile(transaction_id: str) -> str:
    return (
        "Customer normally transfers under £5,000. "
        "This transaction is £47,000 and first to international counterparty."
    )


@function_tool(needs_approval=True)
async def escalate_to_human(report: str) -> str:
    print("\n--- ESCALATION REPORT ---")
    print(report)
    return "Case escalated to Financial Crime team."


# ---- Investigation Agent ----

investigation_agent = Agent(
    name="investigation_agent",
    instructions="""
You are a senior AML investigation agent.

You do NOT detect fraud yourself.
You rely entirely on detection systems and intelligence tools.

Your job:
1. Call ALL tools.
2. Fuse the signals into a coherent explanation.
3. Estimate overall fraud probability.
4. If probability > threshold, escalate with written report.
5. Otherwise, clear the transaction.

Think like a financial crime analyst.
""",
    model_settings=ModelSettings(tool_choice="required"),
    tools=[
        internal_fraud_model,
        vendor_fraud_platform,
        data_fusion_cross_bank,
        customer_behavior_profile,
        escalate_to_human,
    ],
)


# ---- Orchestrator ----

orchestrator = Agent(
    name="aml_orchestrator",
    instructions="""
You orchestrate AML investigations.
You never invent evidence.
You always base conclusions on tool outputs.
""",
    tools=[
        investigation_agent.as_tool(
            tool_name="run_investigation",
            tool_description="Run a full AML investigation",
            needs_approval=True,
        )
    ],
)


# ---- Demo Runner ----

async def main():
    print("\n=== AML Investigation (Realistic Architecture) ===\n")

    tx_id = input_with_fallback(
        "Enter suspicious transaction ID: ",
        "TX-883742"
    )

    context = RunContextWrapper(
        InvestigationContext(transaction_id=tx_id)
    )

    print("\nRunning investigation...\n")

    with trace("AML Investigation"):
        result = await Runner.run(
            starting_agent=orchestrator,
            input=f"Investigate transaction {tx_id}",
            context=context.context,
        )

        # Human-in-the-loop
        while result.interruptions:
            async def confirm(question: str) -> bool:
                return confirm_with_fallback(
                    f"{question} (y/n): ",
                    default=True
                )

            state = result.to_state()
            for interruption in result.interruptions:
                prompt = (
                    f"\nApprove tool call: {interruption.name} "
                    f"with arguments {interruption.arguments}?"
                )
                approved = await confirm(prompt)
                if approved:
                    state.approve(interruption)
                    print(f"✓ Approved: {interruption.name}")
                else:
                    state.reject(interruption)
                    print(f"✗ Rejected: {interruption.name}")

            result = await Runner.run(orchestrator, state)

    print("\n=== FINAL OUTCOME ===")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())