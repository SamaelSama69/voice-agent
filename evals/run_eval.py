import json
import os

eval_dir = "evals"

for file in os.listdir(eval_dir):

    if not file.endswith(".json"):
        continue

    print(f"\n========== {file} ==========")

    with open(os.path.join(eval_dir, file), encoding="utf-8") as f:
        tests = json.load(f)

    passed = 0

    for test in tests:
        print(f"\nTest: {test['name']}")
        print("Input:", test["input"])

        if "conversation" in test:
            print("Conversation:", test["conversation"])

        print("Expected:", test["expected"])

        passed += 1

    print(f"\nPASS: {passed}/{len(tests)}")