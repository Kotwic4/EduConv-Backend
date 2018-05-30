create table datasets(
id INTEGER PRIMARY KEY,
name TEXT,
train_images_count INTEGER,
test_images_count INTEGER,
img_width INTEGER,
img_height INTEGER,
dir_path TEXT,
labels TEXT
);


create table models(
id INTEGER PRIMARY KEY,
dataset_id INTEGER,
epochs_learnt INTEGER DEFAULT 0,
epochs_to_learn INTEGER DEFAULT 0,
dir_path TEXT,
FOREIGN KEY(dataset_id) REFERENCES datasets(id)
);

