import datetime
from typing import Optional
import databases
import sqlalchemy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

# Create a database connection
database = databases.Database('sqlite+aiosqlite:///foto.db')

# Define the database tables
metadata = sqlalchemy.MetaData()
users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("img", sqlalchemy.String),
    sqlalchemy.Column("bgImg", sqlalchemy.String),
    sqlalchemy.Column("about", sqlalchemy.String),
)
posts_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("authorId", sqlalchemy.Integer),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("posted", sqlalchemy.Date),
    sqlalchemy.Column("content", sqlalchemy.String),
    sqlalchemy.Column("img", sqlalchemy.String),
    sqlalchemy.ForeignKeyConstraint(["authorId"], ["users.id"]),
)
tags_table = sqlalchemy.Table(
    "tags",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("postId", sqlalchemy.Integer),
    sqlalchemy.Column("tag", sqlalchemy.String),
    sqlalchemy.ForeignKeyConstraint(["postId"], ["posts.id"]),
)
comments_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("postId", sqlalchemy.Integer),
    sqlalchemy.Column("authorId", sqlalchemy.Integer),
    sqlalchemy.Column("content", sqlalchemy.String),
    sqlalchemy.ForeignKeyConstraint(["postId"], ["posts.id"]),
    sqlalchemy.ForeignKeyConstraint(["authorId"], ["users.id"]),
)
likes_table = sqlalchemy.Table(
    "likes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("postId", sqlalchemy.Integer),
    sqlalchemy.Column("userId", sqlalchemy.Integer),
    sqlalchemy.ForeignKeyConstraint(["postId"], ["posts.id"]),
    sqlalchemy.ForeignKeyConstraint(["userId"], ["users.id"]),
)
saved_table = sqlalchemy.Table(
    "saved",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("postId", sqlalchemy.Integer),
    sqlalchemy.Column("userId", sqlalchemy.Integer),
    sqlalchemy.ForeignKeyConstraint(["postId"], ["posts.id"]),
    sqlalchemy.ForeignKeyConstraint(["userId"], ["users.id"]),
)
follows_table = sqlalchemy.Table(
    "follows",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("followerId", sqlalchemy.Integer),
    sqlalchemy.Column("followingId", sqlalchemy.Integer),
    sqlalchemy.ForeignKeyConstraint(["followerId"], ["users.id"]),
    sqlalchemy.ForeignKeyConstraint(["followingId"], ["users.id"]),
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    try:
        yield
    finally:
        await database.disconnect()

# Create the FastAPI app
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# /api/login

@app.post("/api/login")
async def login(cred: dict):
    user = await database.fetch_one(users_table.select().where(users_table.c.email == cred['email']).where(users_table.c.password == cred['password']))
    return user

# /api/users/...

@app.get("/api/users")
async def get_all_users():
    users = await database.fetch_all(users_table.select())
    return users

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    user = await database.fetch_one(users_table.select().where(users_table.c.id == user_id))
    return user

@app.post("/api/users")
async def create_user(user: dict):
    user_id = await database.execute(users_table.insert().values(user))
    return {**user, "id": user_id}

@app.put("/api/users/{user_id}")
async def update_user(user_id: int, user: dict):
    await database.execute(users_table.update().where(users_table.c.id == user_id).values(user))
    return {**user, "id": user_id}

# /api/posts/...

@app.get("/api/posts")
async def get_posts(skip: Optional[int] = 0, limit: Optional[int] = None):
    if limit is None:
        query = posts_table\
                .select()\
                .outerjoin(tags_table, tags_table.c.postId == posts_table.c.id)\
                .group_by(posts_table.c.id)\
                .add_columns(sqlalchemy.func.group_concat(tags_table.c.tag).label("tags"))\
                .order_by(posts_table.c.posted.desc())\
                .offset(skip)
        print(query)
        posts = await database.fetch_all(query)
    else:
        query = posts_table\
                .select()\
                .outerjoin(tags_table, tags_table.c.postId == posts_table.c.id)\
                .group_by(posts_table.c.id)\
                .add_columns(sqlalchemy.func.group_concat(tags_table.c.tag).label("tags"))\
                .order_by(posts_table.c.posted.desc())\
                .offset(skip)\
                .limit(limit)
        print(query)
        posts = await database.fetch_all(query)
    return posts

@app.get("/api/posts/{post_id}")
async def get_post(post_id: int):
    post = await database.fetch_one(posts_table\
                                    .select()\
                                    .outerjoin(tags_table, tags_table.c.postId == posts_table.c.id)\
                                    .group_by(posts_table.c.id)\
                                    .add_columns(sqlalchemy.func.group_concat(tags_table.c.tag).label("tags"))\
                                    .where(posts_table.c.id == post_id))
    return post

@app.post("/api/posts")
async def create_post(post: dict):
    post_tags = post.pop("tags", [])
    post["posted"] = datetime.date.fromisoformat(post["posted"])
    post_id = await database.execute(posts_table.insert().values(post))

    for tag in post_tags:
        await database.execute(tags_table.insert().values({"postId": post_id, "tag": tag}))

    return {**post, "id": post_id}

@app.put("/api/posts/{post_id}")
async def update_post(post_id: int, post: dict):
    post_tags = post.pop("tags", [])
    post["posted"] = datetime.date.fromisoformat(post["posted"])
    old_tags = await database.fetch_all(tags_table.select().where(tags_table.c.postId == post_id))
    old_tags = list(map(lambda tag: tag._mapping, old_tags))

    for deleted_tag in list(filter(lambda tag: tag["tag"] not in post_tags, old_tags)):
        await database.execute(tags_table.delete().where(tags_table.c.id == deleted_tag["id"]))

    for new_tag in list(filter(lambda tag: tag not in [old_tag["tag"] for old_tag in old_tags], post_tags)):
        await database.execute(tags_table.insert().values({"postId": post_id, "tag": new_tag}))

    await database.execute(posts_table.update().where(posts_table.c.id == post_id).values(post))

    return {**post, "id": post_id}

@app.delete("/api/posts/{post_id}")
async def delete_post(post_id: int):
    await database.execute(posts_table.delete().where(posts_table.c.id == post_id))
    return {"message": "Post deleted"}

# /api/posts/{post_id}/comments/...

@app.get("/api/posts/{post_id}/comments")
async def get_comments(post_id: int, skip: Optional[int] = 0, limit: Optional[int] = None):
    if limit is None:
        comments = await database.fetch_all(comments_table.select().where(comments_table.c.postId == post_id).order_by(-comments_table.c.id).offset(skip))
    else:
        comments = await database.fetch_all(comments_table.select().where(comments_table.c.postId == post_id).order_by(-comments_table.c.id).offset(skip).limit(limit))
    return comments

@app.post("/api/posts/{post_id}/comments")
async def create_comment(post_id: int, comment: dict):
    comment_id = await database.execute(comments_table.insert().values({**comment, "postId": post_id}))
    return {**comment, "id": comment_id}

# /api/posts/{post_id}/likes/...

@app.get("/api/posts/{post_id}/likes")
async def get_likes_count(post_id: int):
    query = sqlalchemy.select(sqlalchemy.func.count().label("count")).select_from(likes_table).where(likes_table.c.postId == post_id)
    likes = await database.fetch_one(query)
    return likes

@app.get("/api/posts/{post_id}/likes/{user_id}")
async def check_like(post_id: int, user_id: int):
    like = await database.fetch_one(likes_table.select().where(likes_table.c.postId == post_id).where(likes_table.c.userId == user_id))
    return {"liked": like is not None}

@app.post("/api/posts/{post_id}/likes/{user_id}")
async def like_post(post_id: int, user_id: int):
    like_id = await database.execute(likes_table.insert().values({"postId": post_id, "userId": user_id}))
    return {"liked": True}

@app.delete("/api/posts/{post_id}/likes/{user_id}")
async def unlike_post(post_id: int, user_id: int):
    await database.execute(likes_table.delete().where(likes_table.c.postId == post_id).where(likes_table.c.userId == user_id))
    return {"message": "Like removed"}

# /api/posts/{post_id}/saved/...

@app.get("/api/posts/{post_id}/saved/{user_id}")
async def check_saved(post_id: int, user_id: int):
    saved = await database.fetch_one(saved_table.select().where(saved_table.c.postId == post_id).where(saved_table.c.userId == user_id))
    return {"saved": saved is not None}

@app.post("/api/posts/{post_id}/saved/{user_id}")
async def save_post(post_id: int, user_id: int):
    saved_id = await database.execute(saved_table.insert().values({"postId": post_id, "userId": user_id}))
    return {"saved": True}

@app.delete("/api/posts/{post_id}/saved/{user_id}")
async def unsave_post(post_id: int, user_id: int):
    await database.execute(saved_table.delete().where(saved_table.c.postId == post_id).where(saved_table.c.userId == user_id))
    return {"message": "Post unsaved"}

# /api/users/{user_id}/posts/...

@app.get("/api/users/{user_id}/posts")
async def get_user_posts(user_id: int):
    posts = await database.fetch_all(posts_table.select().where(posts_table.c.authorId == user_id))
    return posts

# /api/users/{user_id}/saved/...

@app.get("/api/users/{user_id}/saved")
async def get_saved_posts(user_id: int):
    saved = await database.fetch_all(saved_table.select().where(saved_table.c.userId == user_id))
    return saved

# /api/users/{user_id}/follows/...

@app.get("/api/users/{user_id}/follows")
async def get_follows(user_id: int):
    follows = await database.fetch_all(follows_table.select().where(follows_table.c.followerId == user_id))
    return follows

@app.get("/api/users/{user_id}/follows/{following_id}")
async def check_follow(user_id: int, following_id: int):
    follow = await database.fetch_one(follows_table.select().where(follows_table.c.followerId == user_id).where(follows_table.c.followingId == following_id))
    return {"followed": follow is not None}

@app.post("/api/users/{user_id}/follows/{following_id}")
async def follow_user(user_id: int, following_id: int):
    follow_id = await database.execute(follows_table.insert().values({"followerId": user_id, "followingId": following_id}))
    return {"followed": True}

@app.delete("/api/users/{user_id}/follows/{following_id}")
async def unfollow_user(user_id: int, following_id: int):
    await database.execute(follows_table.delete().where(follows_table.c.followerId == user_id).where(follows_table.c.followingId == following_id))
    return {"message": "User unfollowed"}

# /api/tags_count

@app.get("/api/tags")
async def get_tags(limit: int = 10):
    query = sqlalchemy.select(tags_table.c.tag).group_by(tags_table.c.tag).order_by(-sqlalchemy.func.count()).limit(limit)
    print(query)
    tags = await database.fetch_all(query)
    return list(map(lambda tag: tag._mapping["tag"], tags))

# /api/search

@app.get("/api/search")
async def search_posts(query: str):
    search_query = f"%{query}%"
    _query = posts_table.select()\
                        .join(tags_table, tags_table.c.postId == posts_table.c.id)\
                        .group_by(posts_table.c.id, posts_table.c.authorId, posts_table.c.title, posts_table.c.posted, posts_table.c.content, posts_table.c.img)\
                        .having(posts_table.c.title.like(search_query) | posts_table.c.content.like(search_query) | sqlalchemy.func.group_concat(tags_table.c.tag).like(search_query))
    posts = await database.fetch_all(_query)
    return posts

app.mount("/", StaticFiles(directory="dist", html=True), name="client")
