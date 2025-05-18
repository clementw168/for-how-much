from pprint import pprint

import requests

BASE_URL = "http://localhost:8000"


if __name__ == "__main__":
    # route = "/categories"

    # response = requests.get(f"{BASE_URL}{route}")
    # pprint(response.json())

    route = "/question_next"

    response = requests.get(
        f"{BASE_URL}{route}",
        params=[("categories", "Travel"), ("categories", "World Impact / Legacy")],
    )
    pprint(response.json())

    # route = "/question/1"

    # response = requests.get(f"{BASE_URL}{route}")
    # pprint(response.json())

    # route = "/question_stats/1"
    # response = requests.get(f"{BASE_URL}{route}")
    # pprint(response.json())

    # route = "/submit_answer"

    # response = requests.post(f"{BASE_URL}{route}", json={"question_id": 1, "answer": 1})
    # pprint(response.json())

    # route = "/question_stats/1"
    # response = requests.get(f"{BASE_URL}{route}")
    # pprint(response.json())
