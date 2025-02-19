## Todo app with FastAPI and React

### Requeirments

- [ ] User should logged in to create, delete and update todo.
- [ ] User should sign up to create an account.
- [ ] User should able to filter or sort their todo by status or priority.
- [ ] User should able to update his info, only the name for now.

### Flow

- [ ] Create a simple landing page the with two buttons login and signup. Login and Signup buttons will navigate users to login and signup pages.
- [ ] After successfully logged in or signed up, user should redirects to dashboard page where he should create, update and sort / filters toods.
- [ ] Dashboard should contains a profile settings for update user info, for now it should be name only.

### Functionality

- [ ] Authentication
- [ ] Create Todo
- [ ] Delete Todo
- [ ] Update Todo
- [ ] Filter/Sort Todo By Priority/Status

### Schema

- User
  - id (unique, string)
  - Name (string)
  - Email (string)
  - Password (string/hashed))
  - createdAt
  - updatedAt
- Todo
  - id (unique, string)
  - userId ref user.id (reference the user)
  - title (string)
  - content (md/text)
  - priority (enum(high,medium,low))
  - status (enum(inprogress, todo, completed))
  - createdAt
  - updatedAt
