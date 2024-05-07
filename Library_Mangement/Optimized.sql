CREATE TABLE Librarian
(
  SSN NUMERIC(9) NOT NULL,
  Name VARCHAR(100) NOT NULL,
  Email VARCHAR(100) NOT NULL,
  Salary NUMERIC(10, 2),
  PRIMARY KEY (SSN)
);

CREATE TABLE Author
(
  Name VARCHAR(100) NOT NULL,
  AuthorID INT NOT NULL,
  PRIMARY KEY (AuthorID)
);

CREATE TABLE Publisher
(
  Name VARCHAR(100) NOT NULL,
  PublisherID INT NOT NULL,
  PRIMARY KEY (PublisherID)
);

CREATE TABLE Address
(
  AddressID INT NOT NULL,
  City VARCHAR(100) NOT NULL,
  State VARCHAR(100) NOT NULL,
  Street VARCHAR(100) NOT NULL,
  Zip_Code NUMERIC(6) NOT NULL,
  PRIMARY KEY (AddressID)
);

CREATE TABLE Client
(
  Email VARCHAR(100) NOT NULL,
  Account_Bal NUMERIC(10, 2),
  Name VARCHAR(100) NOT NULL,
  ClientID INT NOT NULL,
  AddressID INT NOT NULL,
  PRIMARY KEY (ClientID),
  FOREIGN KEY (AddressID) REFERENCES Address(AddressID)
);

CREATE TABLE Document
(
  DocID INT NOT NULL,
  Year CHAR(4) NOT NULL,
  Type VARCHAR(100) NOT NULL,
  Num_Copies INT NOT NULL,
  AuthorID INT NOT NULL,
  PublisherID INT NOT NULL,
  PRIMARY KEY (DocID),
  FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID),
  FOREIGN KEY (PublisherID) REFERENCES Publisher(PublisherID)
);

CREATE TABLE Book
(
  ISBN VARCHAR(100) NOT NULL,
  Edition VARCHAR(100) NOT NULL,
  Num_of_Pages INT NOT NULL,
  Title VARCHAR(100) NOT NULL,
  DocID INT NOT NULL,
  PRIMARY KEY (DocID),
  FOREIGN KEY (DocID) REFERENCES Document(DocID)
);

CREATE TABLE Journal_Article
(
  Issue VARCHAR(100) NOT NULL,
  Article_Title VARCHAR(100) NOT NULL,
  Journal_Name VARCHAR(100) NOT NULL,
  Issue_num VARCHAR(100) NOT NULL,
  DocID INT NOT NULL,
  PRIMARY KEY (DocID),
  FOREIGN KEY (DocID) REFERENCES Document(DocID)
);

CREATE TABLE Magazine
(
  Title VARCHAR(100) NOT NULL,
  ISBN VARCHAR(100) NOT NULL,
  Month VARCHAR(100) NOT NULL,
  Magazine_Name_ VARCHAR(100) NOT NULL,
  DocID INT NOT NULL,
  PRIMARY KEY (DocID),
  FOREIGN KEY (DocID) REFERENCES Document(DocID)
);

CREATE TABLE Credit_Card
(
  Card_Num NUMERIC(16) NOT NULL,
  AddressID INT NOT NULL,
  ClientID INT NOT NULL,
  PRIMARY KEY (Card_Num),
  FOREIGN KEY (AddressID) REFERENCES Address(AddressID),
  FOREIGN KEY (ClientID) REFERENCES Client(ClientID)
);

CREATE TABLE ElectronicCopy
(
  ECopyID INT NOT NULL,
  LendDate DATE NOT NULL,
  DocID INT NOT NULL,
  ClientID INT NOT NULL,
  PRIMARY KEY (ECopyID),
  FOREIGN KEY (DocID) REFERENCES Document(DocID),
  FOREIGN KEY (ClientID) REFERENCES Client(ClientID)
);

CREATE TABLE Copy
(
  CopyID INT NOT NULL,
  LendDate DATE NOT NULL,
  Available INT NOT NULL,
  DocID INT NOT NULL,
  ClientID INT NOT NULL,
  PRIMARY KEY (CopyID),
  FOREIGN KEY (DocID) REFERENCES Document(DocID),
  FOREIGN KEY (ClientID) REFERENCES Client(ClientID)
);