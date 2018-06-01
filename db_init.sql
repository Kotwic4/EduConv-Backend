create table datasets(
id INTEGER PRIMARY KEY,
name TEXT,
train_images_count INTEGER,
test_images_count INTEGER,
img_width INTEGER,
img_height INTEGER,
img_depth INTEGER,
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

insert into datasets(name,train_images_count,test_images_count,img_width,img_height,img_depth,dir_path,labels) values ("mnist",60000,10000,28,28,1,"","[0,1,2,3,4,5,6,7,8,9]")
