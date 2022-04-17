import motor.motor_asyncio
import os
from urllib.parse import unquote

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_AUTH"))
db = client["xontex"]


def jawaban_helper(jawaban) -> dict:
    return {
        # "id": str(jawaban["_id"]),
        "soal": jawaban["soal"],
        "jawab": jawaban["jawab"],
    }


async def retrieve_jawaban(mapel: str, soal: str) -> dict:
    result = await db[mapel].find_one({"soal": soal})
    if result:
        return jawaban_helper(result)


# async def retrieve_all_jawaban(mapel: str) -> dict:
#     result = await db[mapel].find({})
#     if result:
#         all_jawaban = [jawaban_helper(x) for x in result]
#         return all_jawaban


async def add_jawaban(mapel: str, jawaban: dict) -> dict:
    test = jawaban["jawaban"]
    format = ["png", "jpg", "jpeg", "webp", "gif"]
    if any(s in test for s in format):
        answer = f"![image]({test})"
    else:
        answer = test

    if not (await db[mapel].find_one({"soal": jawaban["soal"]})):
        await db[mapel].insert_one(
            {
                "soal": jawaban["soal"],
                "jawab": [{"username": jawaban["username"], "jawaban": answer}],
            }
        )
        result = await db[mapel].find_one({"soal": jawaban["soal"]})
        return jawaban_helper(result)

    if await db[mapel].find_one(
        {
            "soal": jawaban["soal"],
            "jawab": {"$elemMatch": {"username": jawaban["username"]}},
        }
    ):
        await db[mapel].update_one(
            {
                "soal": jawaban["soal"],
                "jawab": {"$elemMatch": {"username": jawaban["username"]}},
            },
            {
                "$set": {
                    "jawab.$": {
                        "username": jawaban["username"],
                        "jawaban": answer,
                    }
                }
            },
        )

    await db[mapel].update_one(
        {
            "soal": jawaban["soal"],
        },
        {
            "$addToSet": {
                "jawab": {
                    "username": jawaban["username"],
                    "jawaban": answer,
                }
            }
        },
    )

    # # old approach
    # if await db[mapel].find_one(
    #     {
    #         "soal": jawaban["soal"],
    #         "jawab": {"$elemMatch": {jawaban["username"]: {"$exists": True}}},
    #     }
    # ):
    #     await db[mapel].update_one(
    #         {
    #             "soal": jawaban["soal"],
    #             "jawab": {"$elemMatch": {jawaban["username"]: {"$exists": True}}},
    #         },
    #         {"$pull": {"jawab": {jawaban["username"]: {"$exists": True}}}},
    #     )
    # # else:
    # await db[mapel].update_one(
    #     {
    #         "soal": jawaban["soal"],
    #         # "jawab": {"$all": [{jawaban["username"]: {"$exists": True}}]},
    #     },
    #     {"$push": {"jawab": {jawaban["username"]: jawaban["jawaban"]}}},
    #     upsert=True,
    # )

    result = await db[mapel].find_one({"soal": jawaban["soal"]})
    return jawaban_helper(result)
