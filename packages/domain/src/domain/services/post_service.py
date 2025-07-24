from bson import ObjectId
from fastapi import Depends

from domain.entities import PostEntity
from domain.repositories import PostRepository, AccountRepository
from domain.usecases import ManagePostUseCase, CreatePostRequest

from infrastructure.queues import RabbitMQConnection


class PostService(ManagePostUseCase):
    def __init__(
        self,
        post_repository: PostRepository = Depends(),
        account_repository: AccountRepository = Depends(),
        queue: RabbitMQConnection = Depends(),
    ):
        self.post_repository = post_repository
        self.account_repository = account_repository
        self.queue = queue

    async def create_post(self, account_id: str, req: CreatePostRequest) -> PostEntity:
        account = await self.account_repository.find_one({"_id": ObjectId(account_id)})
        if not account:
            raise ValueError("Owner account does not exist 🐶")

        post = PostEntity.create(
            account_id=account_id,
            image_url=req.image_url,
            title=req.title,
            captions=req.captions,
            tags=req.tags,
        )

        await self.queue.send_messages(
            {
                "account_id": account_id,
                "message": "New post created",
            },
            "agrismart.notifications",
        )

        print(f"Creating post: {post}")
        # return await self.post_repository.create(post)
        return post
