import sys
from pydantic_ai.exceptions import UsageLimitExceeded
from pydantic_ai import UsageLimits
from src.agent import build_agent, Deps

def print_attempt(i: int, attempt) -> None:
    status = "PASSED" if attempt.ok else "FAILED"
    print(f"\n--- Attempt {i+1} {status} ---")
    if not attempt.ok:
        print(attempt.output)

def main() -> None:
    task = " ".join(sys.argv[1:]) or input("Task: ")
    agent = build_agent()
    deps = Deps()

    print(f"\nWorking on: {task}\n")
    try:
        result = agent.run_sync(
            task,
            deps=deps,
            usage_limits=UsageLimits(request_limit=8)
        )
    except UsageLimitExceeded:
        print("Agent exhausted its request budget without passing.")
        sys.exit(1)

    for i, attempt in enumerate(deps.attempts):
        print_attempt(i, attempt)

    print(f"\nDone in {len(deps.attempts)} attempt(s)")
    print(f"\nSummary: {result.output.summary}")
    print(f"\n--- Final Code ---\n{result.output.code}")

if __name__ == "__main__":
    main()