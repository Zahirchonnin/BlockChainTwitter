# @version ^0.2.8


struct Tweet:
    message: String[280]
    _addr: address
    date: uint256

tweets: HashMap[uint256, Tweet]
tweets_count: uint256

users_data: HashMap[address, String[30]]
users_addr: address[10]
user: address
userus_num: uint256


@external
def __init__():
    self.tweets_count = 0
    self.userus_num = 0

@external
def getName() -> String[30]:
    assert msg.sender in self.users_addr, '!You not singed in.'
    return self.users_data[msg.sender]

@external
def SingUp(name: String[30]):
    assert not msg.sender in self.users_addr, '!You already singed in'
    self.users_data[msg.sender] = name
    self.users_addr[self.userus_num] = msg.sender
    self.userus_num += 1

@external
def logIn():
    assert msg.sender in self.users_addr, '!You are not singed in'
    self.user = msg.sender

@external
def newTweet(tweet: String[280], date: uint256):
    assert msg.sender == self.user, '!Sing in first.'
    self.tweets[self.tweets_count].message = tweet
    self.tweets[self.tweets_count]._addr = msg.sender
    self.tweets[self.tweets_count].date = date
    self.tweets_count += 1