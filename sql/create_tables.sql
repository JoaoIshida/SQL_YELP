CREATE TABLE business (
    business_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT NOT NULL,
    postal_code TEXT,
    stars REAL CHECK (stars >= 1 AND stars <= 5),
    review_count INTEGER DEFAULT 0 CHECK (review_count >= 0)
);

CREATE TABLE checkin (
    checkin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE user_yelp (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    review_count INTEGER DEFAULT 0 CHECK (review_count >= 0),
    yelping_since DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    useful INTEGER DEFAULT 0 CHECK (useful >= 0),
    funny INTEGER DEFAULT 0 CHECK (funny >= 0),
    cool INTEGER DEFAULT 0 CHECK (cool >= 0),
    fans INTEGER DEFAULT 0 CHECK (fans >= 0),
    average_stars REAL CHECK (average_stars >= 1 AND average_stars <= 5)
);

CREATE TABLE tip (
    tip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    business_id TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    compliment_count INTEGER DEFAULT 0 CHECK (compliment_count >= 0),
    FOREIGN KEY (user_id) REFERENCES user_yelp(user_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE friendship (
    user_id TEXT,
    friend TEXT,
    PRIMARY KEY (user_id, friend),
    FOREIGN KEY (user_id) REFERENCES user_yelp(user_id),
    FOREIGN KEY (friend) REFERENCES user_yelp(user_id)
);

CREATE TABLE review (
    review_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    business_id TEXT NOT NULL,
    stars INTEGER NOT NULL CHECK (stars >= 1 AND stars <= 5),
    useful INTEGER DEFAULT 0 CHECK (useful >= 0),
    funny INTEGER DEFAULT 0 CHECK (funny >= 0),
    cool INTEGER DEFAULT 0 CHECK (cool >= 0),
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_yelp(user_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);