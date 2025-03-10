import yaml

from utils import num_tokens_from_string, calc_input, calc_output, calc_cost


with open("src/ra.yaml", "r", encoding="utf-8") as f:
    logs = yaml.safe_load(f)

def main():
    rag_ref = logs.get("rag_ref", "")
    rag_legal = logs.get("rag_legal", "")
    input_system = logs.get("input_system", "")
    input_user = logs.get("input_user", "")
    output = logs.get("output", "")

    total_cost = .0
    total_cost += calc_cost(rag_ref, 'text-embedding-ada-002')
    total_cost += calc_cost(rag_legal, 'text-embedding-ada-002')
    total_cost += calc_input(input_system, 'gpt-4o')
    total_cost += calc_input(input_user, 'gpt-4o')
    total_cost += calc_output(output, 'gpt-4o')
    print(f"Total Cost: ${total_cost:,.2f}")

if __name__ == "__main__":
    main()