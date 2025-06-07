from pprint import pprint

import requests

BASE_URL = "http://localhost:8000"


token = "1db36020-e63f-4917-bf57-16c46b2873b1"
headers = {"Authorization": f"Bearer {token}"}

question_id = 254

if __name__ == "__main__":
    # route = "/users/all"
    # response = requests.get(f"{BASE_URL}{route}")
    # pprint(response.json())

    # route = "/user/new"
    # response = requests.post(f"{BASE_URL}{route}")
    # print(response)
    # pprint(response.json())

    # route = "/user/me"
    # response = requests.get(f"{BASE_URL}{route}", headers=headers)
    # pprint(response.json())

    # route = "/categories"
    # response = requests.get(f"{BASE_URL}{route}", headers=headers)
    # pprint(response.json())

    # route = "/question_next"
    # response = requests.get(
    #     f"{BASE_URL}{route}",
    #     params=[("categories", "Travel"), ("categories", "World Impact / Legacy")],
    #     headers=headers,
    # )
    # print(response)
    # pprint(response.json())

    # route = "/question/1"
    # response = requests.get(f"{BASE_URL}{route}", headers=headers)
    # print(response)
    # pprint(response.json())

    # route = "/question_stats/1"
    # response = requests.get(f"{BASE_URL}{route}")
    # pprint(response.json())

    route = "/submit_answer"
    response = requests.post(
        f"{BASE_URL}{route}",
        json={"question_id": question_id, "answer": 1},
        headers=headers,
    )
    pprint(response.json())

    route = "/user/me"
    response = requests.get(f"{BASE_URL}{route}", headers=headers)
    pprint(response.json())

    # route = "/question_stats/1"
    # response = requests.get(f"{BASE_URL}{route}")
    # pprint(response.json())
