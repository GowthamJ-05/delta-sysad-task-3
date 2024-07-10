create database QuizzMasters;
use QuizzMasters;

create table Userbase (
    username varchar(40) primary key ,
    password varchar(100)
);

create table Leaderboard (
    username varchar(40) primary key,
    points int default 0,
    number_qns int default 0,
    foreign key (username) references Userbase(username)
);

create table QuestionBank (
    qid int auto_increment primary key ,
    question varchar(150),
    option1 varchar(30),
    option2 varchar(30) ,
    option3 varchar(30),
    option4 varchar(30),
    correct_option int,
    username varchar(40),
    allotted_for json,
    foreign key (username) references Userbase(username)
);


