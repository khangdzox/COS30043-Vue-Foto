import random
import sqlite3

# Prepare connection
con = sqlite3.connect('foto.db')
cur = con.cursor()

# Prepare tables
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT,
    img TEXT,
    bgImg TEXT,
    about TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    authorId INTEGER,
    title TEXT,
    posted DATE,
    content TEXT,
    img TEXT,
    FOREIGN KEY(authorId) REFERENCES users(id) ON DELETE CASCADE
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    postId INTEGER,
    tag TEXT,
    FOREIGN KEY(postId) REFERENCES posts(id) ON DELETE CASCADE
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    postId INTEGER,
    authorId INTEGER,
    content TEXT,
    FOREIGN KEY(postId) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(authorId) REFERENCES users(id) ON DELETE CASCADE
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    postId INTEGER,
    userId INTEGER,
    FOREIGN KEY(postId) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(userId) REFERENCES users(id) ON DELETE CASCADE
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS saved (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    postId INTEGER,
    userId INTEGER,
    FOREIGN KEY(postId) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(userId) REFERENCES users(id) ON DELETE CASCADE
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS follows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    followerId INTEGER,
    followingId INTEGER,
    FOREIGN KEY(followerId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(followingId) REFERENCES users(id) ON DELETE CASCADE
)
''')

# Insert demo data
users = [
    (
        1,
        "John Doe",
        "john@doe.com",
        "!QAZ2wsx",
        "https://randomuser.me/api/portraits/men/85.jpg",
        "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe",
        "Hi, I'm John Doe. I'm a web developer and I love to create new things. I'm a big fan of Vue and I'm always looking for new projects to work on. Feel free to contact me if you have any questions or if you'd like to work together."
    ),
    (
        2,
        "Alex Smith",
        "alex@smith.net",
        "!QAZ3edc",
        "https://randomuser.me/api/portraits/men/4.jpg",
        "https://images.unsplash.com/photo-1574169208507-84376144848b",
        ""
    ),
    (
        3,
        "Sara Watson",
        "sara@watson.org",
        "!QAZ4rfv",
        "",
        "",
        ""
    )
]
cur.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)', users)

posts = [
    (
        1,
        1,
        "Beautiful nature in my backyard",
        "2019-01-01",
        "I love the nature in my backyard. It's so beautiful and peaceful. I can sit here for hours and just enjoy the view. I'm so grateful to have this in my life.",
        "https://picsum.photos/id/28/3000/4000"
    ),
    (
        2,
        2,
        "Working right now",
        "2019-01-02",
        "I'm working right now. I have so much to do and so little time. I wish I could just relax and enjoy the day. But I have to work. I have to make money. I have to survive.",
        "https://picsum.photos/id/1/3670/2670"
    ),
    (
        3,
        3,
        "Feeling happy today",
        "2019-01-03",
        "I'm feeling happy today. I don't know why. I just feel good. I feel like everything is going to be okay. I feel like I can do anything. I feel like I'm on top of the world.",
        "https://picsum.photos/id/64/5000/3000"
    ),
    (
        4,
        1,
        "Feeling sad today",
        "2019-01-04",
        "I'm feeling sad today. I don't know why. I just feel bad. I feel like everything is going wrong. I feel like I can't do anything. I feel like I'm at the bottom of the world.",
        "https://picsum.photos/id/100/5000/4000"
    ),
    (
        5,
        2,
        "Feeling angry today",
        "2019-01-05",
        "I'm feeling angry today. I don't know why. I just feel mad. I feel like everything is pissing me off. I feel like I can't control myself. I feel like I'm going to explode.",
        "https://picsum.photos/id/200/600/300"
    ),
    (
        6,
        3,
        "Meet my cat Danny",
        "2019-01-06",
        "This is my cat Danny. He's so cute and fluffy. I love him so much. He's my best friend. He's always there for me when I need him. I don't know what I would do without him.",
        "https://picsum.photos/id/40/550/350"
    ),
    (
        7,
        1,
        "Meet my dog Max",
        "2019-01-07",
        "This is my dog Max. He's so loyal and friendly. I love him so much. He's my best friend. He's always there for me when I need him. I don't know what I would do without him.",
        "https://picsum.photos/id/400/5000/4500"
    ),
    (
        8,
        2,
        "The strongholds of the enemy",
        "2019-01-08",
        "The strongholds of the enemy are all around us. They are in our minds, our hearts, our souls. They are in our homes, our schools, our workplaces. They are in our churches, our communities, our nations. We must stand firm against them. We must resist them. We must fight them. We must destroy them.",
        "https://picsum.photos/id/500/5000/5000"
    ),
    (
        9,
        3,
        "The power of love",
        "2019-01-09",
        "The power of love is greater than the power of hate. The power of love is greater than the power of fear. The power of love is greater than the power of death. The power of love is greater than the power of evil. The power of love is greater than the power of anything in this world.",
        "https://picsum.photos/id/600/5000/3000"
    ),
    (
        10,
        1,
        "The beauty of life",
        "2019-01-10",
        "The beauty of life is all around us. It's in the flowers, the trees, the birds, the bees. It's in the sun, the moon, the stars, the seas. It's in the mountains, the valleys, the rivers, the lakes. It's in the people, the animals, the plants, the rocks. It's in everything we see, hear, touch, taste, smell. It's in everything we are, do, say, think, feel. It's in everything we know, believe, hope, dream, love. It's in everything we are and everything we can be.",
        "https://picsum.photos/id/700/5000/4000"
    ),
    (
        11,
        1,
        "Beautiful nature in my backyard",
        "2019-01-01",
        "I love the nature in my backyard. It's so beautiful and peaceful. I can sit here for hours and just enjoy the view. I'm so grateful to have this in my life.",
        "https://picsum.photos/id/28/3000/4000"
    ),
    (
        12,
        2,
        "Working right now",
        "2019-01-02",
        "I'm working right now. I have so much to do and so little time. I wish I could just relax and enjoy the day. But I have to work. I have to make money. I have to survive.",
        "https://picsum.photos/id/1/3670/2670"
    ),
    (
        13,
        3,
        "Feeling happy today",
        "2019-01-03",
        "I'm feeling happy today. I don't know why. I just feel good. I feel like everything is going to be okay. I feel like I can do anything. I feel like I'm on top of the world.",
        "https://picsum.photos/id/64/5000/3000"
    ),
    (
        14,
        1,
        "Feeling sad today",
        "2019-01-04",
        "I'm feeling sad today. I don't know why. I just feel bad. I feel like everything is going wrong. I feel like I can't do anything. I feel like I'm at the bottom of the world.",
        "https://picsum.photos/id/100/5000/4000"
    ),
    (
        15,
        2,
        "Feeling angry today",
        "2019-01-05",
        "I'm feeling angry today. I don't know why. I just feel mad. I feel like everything is pissing me off. I feel like I can't control myself. I feel like I'm going to explode.",
        "https://picsum.photos/id/200/6000/3000"
    ),
    (
        16,
        3,
        "Meet my cat Danny",
        "2019-01-06",
        "This is my cat Danny. He's so cute and fluffy. I love him so much. He's my best friend. He's always there for me when I need him. I don't know what I would do without him.",
        "https://picsum.photos/id/300/5500/3500"
    ),
    (
        17,
        1,
        "Meet my dog Max",
        "2019-01-07",
        "This is my dog Max. He's so loyal and friendly. I love him so much. He's my best friend. He's always there for me when I need him. I don't know what I would do without him.",
        "https://picsum.photos/id/400/5000/4500"
    ),
    (
        18,
        2,
        "The strongholds of the enemy",
        "2019-01-08",
        "The strongholds of the enemy are all around us. They are in our minds, our hearts, our souls. They are in our homes, our schools, our workplaces. They are in our churches, our communities, our nations. We must stand firm against them. We must resist them. We must fight them. We must destroy them.",
        "https://picsum.photos/id/500/5000/5000"
    ),
    (
        19,
        3,
        "The power of love",
        "2019-01-09",
        "The power of love is greater than the power of hate. The power of love is greater than the power of fear. The power of love is greater than the power of death. The power of love is greater than the power of evil. The power of love is greater than the power of anything in this world.",
        "https://picsum.photos/id/600/5000/3000"
    ),
    (
        20,
        1,
        "The beauty of life",
        "2019-01-10",
        "The beauty of life is all around us. It's in the flowers, the trees, the birds, the bees. It's in the sun, the moon, the stars, the seas. It's in the mountains, the valleys, the rivers, the lakes. It's in the people, the animals, the plants, the rocks. It's in everything we see, hear, touch, taste, smell. It's in everything we are, do, say, think, feel. It's in everything we know, believe, hope, dream, love. It's in everything we are and everything we can be.",
        "https://picsum.photos/id/700/5000/4000"
    )
]
cur.executemany('INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?)', posts)

tags = [
    (1, 1, "nature"),
    (2, 1, "backyard"),
    (3, 1, "beautiful"),
    (4, 1, "peaceful"),
    (5, 2, "work"),
    (6, 2, "money"),
    (7, 2, "stress"),
    (8, 2, "pressure"),
    (9, 3, "happiness"),
    (10, 3, "positive"),
    (11, 4, "sadness"),
    (12, 4, "negative"),
    (13, 5, "anger"),
    (14, 5, "frustration"),
    (15, 6, "pets"),
    (16, 6, "cats"),
    (17, 7, "pets"),
    (18, 7, "dogs"),
    (19, 8, "enemy"),
    (20, 8, "resistance"),
    (21, 9, "love"),
    (22, 9, "power"),
    (23, 10, "beauty"),
    (24, 10, "life")
]
cur.executemany('INSERT INTO tags VALUES (?, ?, ?)', tags)

comments = [
    (
        1,
        1,
        1,
        "Wow this is great!"
    ),
    (
        2,
        1,
        2,
        "I love this!"
    ),
    (
        3,
        1,
        3,
        "How do I get started? This is amazing! I love it! Can't wait to get started!"
    ),
    (
        4,
        1,
        1,
        "I'm so excited to get started! Last time I tried to do this, I failed miserably. I'm so excited to get started!"
    ),
    (
        5,
        1,
        2,
        "This is really cool! I love it! When I first started, I was so nervous. But now I'm so excited to get started!"
    ),
    (
        6,
        1,
        3,
        "I'm so excited to get started! I can't wait to get started! I'm so excited to get started!"
    )
]
cur.executemany('INSERT INTO comments VALUES (?, ?, ?, ?)', comments)

likes = []
for postId in range(1, 21):
    for userId in range(1, 4):
        if random.random() < 0.5:
            likes.append((None, postId, userId))
cur.executemany('INSERT INTO likes VALUES (?, ?, ?)', likes)

saved = []
for postId in range(1, 21):
    userId = random.randint(1, 3)
    saved.append((None, postId, userId))
cur.executemany('INSERT INTO saved VALUES (?, ?, ?)', saved)

follows = []
for followerId in range(1, 4):
    for followingId in range(1, 4):
        if followerId != followingId and random.random() < 0.5:
            follows.append((None, followerId, followingId))

# Commit and close
con.commit()
con.close()
