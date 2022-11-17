## <remove all of the example text and notes in < > such as this one>

## Functional Requirements

1. Login
2. Logout
3. Create new account
4. Delete account
5. User homepage
6. Send messages to followers
7. Create a Post
8. Delete a Post
9. Edit a Post
10. Like/Dislike/Comment a Post
11. Follow User
12. Search for User

## Non-functional Requirements
1. Speed - We would want the homepage to load up in under 2 seconds.
2. Data Security (encrpyt user information)
3. Compatibility: We want our site to be responsive on all devices. Use features that every browser supports.
4. scalability

## Use Cases

1. Use Case Name (Should match functional requirement name)
- **Pre-condition:** <can be a list or short description> Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua.

- **Trigger:** <can be a list or short description> Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. 

- **Primary Sequence:**
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Et sequi incidunt 
  3. Quis aute iure reprehenderit
  4. ... 
  5. ...
  6. ...
  7. ...
  8. ...
  9. ...
  10. <Try to stick to a max of 10 steps>

- **Primary Postconditions:** <can be a list or short description> 

- **Alternate Sequence:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

- **Alternate Sequence <optional>:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

2. Use Case Name (Should match functional requirement name)
   ...

4. Follow User
- **Pre-condition:** The User can't already be followed and they must view the user's profile to follow

- **Trigger:** They must click the big follow button when viewing the User's profile

- **Primary Sequence:**
  
  1. Click on the User they want to follow to view their profile
  2. Once on their profile page, click on the big follow button

- **Primary Postconditions:** Nothing. This task is only used for following people, nothing more

- **Alternate Sequence:** User is already followed - UnFollow
  
  1. Click on the User they want to follow to view their profile
  2. The big follow button will now be UnFollow, they can choose to click the button and UnFollow the User

5. Search for User
- **Pre-condition:** No big conditions. There should be a search bar at the top on all pages (navbar)

- **Trigger:** They click on the search bar and start typing

- **Primary Sequence:**
  
  1. Click on the search bar at the top of every page
  2. Type in the name of the User you want to search for
  3. The User should pop up as an option and they click on the user

- **Primary Postconditions:** There are many things they can do after they search for the user. Some choices are listed below

  1. Follow/UnFollow the user
  2. Message the User
  3. Like/dislike/comment on the User's posts

- **Alternate Sequence:** User does not exist
  
  1. Click on the search bar at the top of every page
  2. Type in the name of the User you want to search for
  3. The User does not exist, so the system prompts a message of "Nothing Here!"

- **Alternate Sequence:** Multiple Users having the same name

  1. Click on the search bar at the top of every page
  2. Type in the name of the User you want to search for 
  3. Mutliple Users with the same name will be listed
  4. Choose one of the User's to click on