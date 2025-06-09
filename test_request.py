from pprint import pprint

import requests

BASE_URL = "http://localhost:8000"


token = "1db36020-e63f-4917-bf57-16c46b2873b1"
headers = {"Authorization": f"Bearer {token}"}

question_id = 254

if __name__ == "__main__":
    route = "/users/all"
    response = requests.get(f"{BASE_URL}{route}")
    pprint(response.json())

    # route = "/user/new"
    # response = requests.post(f"{BASE_URL}{route}")
    # print(response)
    # pprint(response.json())

    # route = "/user/me"
    # response = requests.get(f"{BASE_URL}{route}", headers=headers)
    # pprint(response.json())

    # route = "/user/reset_questions"
    # response = requests.post(
    #     f"{BASE_URL}{route}",
    #     json=[254, 602],
    #     headers=headers,
    # )
    # pprint(response.json())

    # route = "/categories"
    # response = requests.get(f"{BASE_URL}{route}", headers=headers)
    # pprint(response.json())

    # route = "/categories/questions"
    # response = requests.get(
    #     f"{BASE_URL}{route}",
    #     params=[("categories", "World Impact / Legacy")],
    #     headers=headers,
    # )
    # print(response)
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

    # route = "/submit_answer"
    # response = requests.post(
    #     f"{BASE_URL}{route}",
    #     json={"question_id": question_id, "answer": 1},
    #     headers=headers,
    # )
    # pprint(response.json())

    # route = "/submit_answer_multiplayer"
    # response = requests.post(
    #     f"{BASE_URL}{route}",
    #     json={"question_id": question_id, "answers": [1, 2, 3, 4, 5]},
    #     headers=headers,
    # )
    # pprint(response.json())

    # route = "/question_stats/1"
    # response = requests.get(f"{BASE_URL}{route}")
    # pprint(response.json())

    # for question_id in [
    #     252,
    #     253,
    #     254,
    #     255,
    #     256,
    #     257,
    #     258,
    #     259,
    #     260,
    #     261,
    #     262,
    #     263,
    #     264,
    #     265,
    #     266,
    # ]:
    #     route = "/submit_answer"
    #     response = requests.post(
    #         f"{BASE_URL}{route}",
    #         json={"question_id": question_id, "answer": 1},
    #         headers=headers,
    #     )
    #     pprint(response.json())

    # route = "/user/me"
    # response = requests.get(f"{BASE_URL}{route}", headers=headers)
    # pprint(response.json())

    # route = "/question_next"
    # response = requests.get(
    #     f"{BASE_URL}{route}",
    #     params=[("categories", "World Impact / Legacy")],
    #     headers=headers,
    # )
    # pprint(response.json())
