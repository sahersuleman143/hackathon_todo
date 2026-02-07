# Browser Testing Guide - Frontend Authentication & Tasks

**Status**: ✅ Frontend Running
**URL**: http://localhost:3000
**Backend**: http://localhost:8000 (API)

---

## 🚀 Quick Start

### 1. Open Your Browser
Navigate to: **http://localhost:3000**

The app will automatically redirect you to `/login` since you're not authenticated.

---

## 📋 Test Checklist

### ✅ Test 1: User Registration

1. **Navigate to**: http://localhost:3000 (will redirect to `/login`)
2. **Look for**: "Sign up" link or registration form
3. **Enter**:
   - Email: `testuser@example.com`
   - Password: `password123` (minimum 8 characters)
4. **Click**: "Sign up" or "Register"

**Expected Results**:
- ✅ No error messages like `[object Object]`
- ✅ Redirects to `/dashboard` automatically
- ✅ Can see task list (empty initially)

**How to Verify**:
- Open Browser Console (F12 → Console)
- Type: `localStorage.getItem('access_token')`
- Should show JWT token like: `eyJhbGciOiJIUzI1NiIs...`

---

### ✅ Test 2: User Login

1. **If already registered**, logout first (or use different email)
2. **Navigate to**: http://localhost:3000/login
3. **Enter**:
   - Email: `testuser@example.com`
   - Password: `password123`
4. **Click**: "Sign in" or "Login"

**Expected Results**:
- ✅ No `Failed to fetch` errors
- ✅ No `[object Object]` in error display
- ✅ Redirects to `/dashboard`
- ✅ Token stored in localStorage

**How to Debug**:
- Open Network Tab (F12 → Network)
- Filter by: `auth`
- Look for POST request to `/api/auth/login`
- Check Response: should have `access_token`

---

### ✅ Test 3: Create Task (Main Test!)

1. **Must be logged in** (complete Test 1 or 2 first)
2. **On Dashboard**: Look for "Create Task" button
3. **Click**: "Create Task" or "Add Task"
4. **Fill Form**:
   - Title: `My First Task`
   - Description: `Testing the authentication fix`
5. **Click**: "Create" or "Submit"

**Expected Results**:
- ✅ NO error: "Not authenticated"
- ✅ NO error: "No token found"
- ✅ Task appears in list immediately
- ✅ No console errors

**How to Verify Authorization Header**:
1. Open Network Tab (F12 → Network)
2. Create a task
3. Click on POST request to `/api/tasks`
4. Check **Request Headers** section
5. Should see: `Authorization: Bearer eyJhbGciOiJIUzI1NiIs...`

**Screenshot This**:
```
Request Headers:
  Authorization: Bearer <your-token-here>
  Content-Type: application/json
```

---

### ✅ Test 4: View Tasks

1. **While logged in**, dashboard should show task list
2. **Should see**: Previously created tasks
3. **Each task shows**:
   - Title
   - Description (truncated if long)
   - Completion status (checkbox)

**Expected Results**:
- ✅ Tasks load without "Not authenticated" error
- ✅ Only YOUR tasks are visible (user isolation)
- ✅ No `[object Object]` rendering issues

---

### ✅ Test 5: Token Persistence

1. **After logging in successfully**
2. **Refresh the page** (F5 or Ctrl+R)
3. **Expected**: Still logged in, see dashboard

4. **Close the browser tab**
5. **Reopen**: http://localhost:3000
6. **Expected**: Still logged in (if token not expired)

**Token Lifespan**: 7 days (per plan.md)

---

### ✅ Test 6: Error Handling

#### Test Invalid Login:
1. Go to http://localhost:3000/login
2. Enter: `wrong@example.com` / `wrongpassword`
3. **Expected**: Clear error message (NOT `[object Object]`)
4. Error should say: "Invalid email or password" or similar

#### Test Create Task Without Token:
1. Open Console (F12)
2. Clear token: `localStorage.removeItem('access_token')`
3. Try to create a task
4. **Expected**:
   - Error message: "Not authenticated"
   - OR redirects to login

---

### ✅ Test 7: Logout

1. **While logged in**, look for "Logout" button
2. **Click**: "Logout"
3. **Expected**:
   - Redirects to `/login`
   - Token removed from localStorage
   - Cannot access `/dashboard` without logging in again

**Verify**:
```javascript
localStorage.getItem('access_token')  // Should be null
```

---

## 🔍 Browser Console Commands

Open Developer Tools (F12) and use these commands:

### Check if Token Exists:
```javascript
localStorage.getItem('access_token')
```

### Check Token Expiry (Decode JWT):
```javascript
const token = localStorage.getItem('access_token');
if (token) {
  const payload = JSON.parse(atob(token.split('.')[1]));
  console.log('Token payload:', payload);
  console.log('User email:', payload.email);
  console.log('User ID:', payload.sub);
}
```

### Test API Call Manually:
```javascript
const token = localStorage.getItem('access_token');
fetch('http://localhost:3000/api/tasks', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(r => r.json())
.then(data => console.log('Tasks:', data))
.catch(err => console.error('Error:', err));
```

### Clear Token (Test Logout):
```javascript
localStorage.removeItem('access_token');
location.reload();
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "Failed to fetch"
**Cause**: Backend not running or CORS issue
**Solution**:
- Check backend: http://localhost:8000
- Should see: `{"message":"Todo API is running","docs":"/docs"}`
- Check `frontend/next.config.js` has proxy rewrites

### Issue 2: "[object Object]" in Error Message
**Cause**: Error not being converted to string
**Status**: ✅ FIXED in LoginForm.tsx
**Verify**: Check lines 32-41 in LoginForm.tsx

### Issue 3: "Not authenticated" when Creating Task
**Cause**: Token not being sent or wrong key
**Status**: ✅ FIXED
- Token key now consistent: `access_token`
- Authorization header auto-included
**Verify**: Check Network tab for Authorization header

### Issue 4: 404 on Root Page
**Cause**: Page routing or app directory issue
**Solution**: Root page redirects to `/login` or `/dashboard`
**Try**: Direct navigation to http://localhost:3000/login

### Issue 5: CORS Errors
**Cause**: Backend CORS or frontend proxy not configured
**Status**: ✅ FIXED
- Backend allows: http://localhost:3000
- Frontend proxies: /api/* → http://localhost:8000/api/*

---

## 📊 What to Check in Network Tab

### For Login Request:
```
Request URL: http://localhost:3000/api/auth/login
Request Method: POST
Status Code: 200 OK

Request Payload:
{
  "username": "testuser@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### For Create Task Request:
```
Request URL: http://localhost:3000/api/tasks
Request Method: POST
Status Code: 201 Created

Request Headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
  Content-Type: application/json

Request Payload:
{
  "title": "My First Task",
  "description": "Testing the authentication fix"
}

Response:
{
  "id": 1,
  "user_id": 11,
  "title": "My First Task",
  "description": "Testing the authentication fix",
  "completed": false,
  "created_at": "2026-02-06T15:29:13.456356",
  "updated_at": "2026-02-06T15:29:13.456356"
}
```

---

## ✅ Success Criteria

All of these should work:

- [ ] Register new user → redirects to dashboard
- [ ] Login existing user → redirects to dashboard
- [ ] Create task → appears in list (no "Not authenticated")
- [ ] View tasks → shows only my tasks
- [ ] Refresh page → still logged in
- [ ] Logout → token cleared, redirects to login
- [ ] Error messages → clear and readable (not `[object Object]`)
- [ ] Authorization header → present in all protected API calls

---

## 🎯 Key Files Changed (Reference)

If you need to review the fixes:

1. **Token Storage**: `frontend/src/lib/auth/hooks.ts:92-109`
2. **Auto Authorization**: `frontend/src/lib/api/client.ts:14-34`
3. **Proxy Config**: `frontend/next.config.js:3-11`
4. **Task Creation**: `frontend/src/components/tasks/CreateTaskForm.tsx:38-50`
5. **Error Handling**: `frontend/src/components/auth/LoginForm.tsx:32-42`

---

## 📸 Take Screenshots Of:

1. Successful login (dashboard view)
2. Network tab showing Authorization header in task creation request
3. Console showing token in localStorage
4. Task list with your created tasks

---

## 🎉 If All Tests Pass:

Congratulations! The authentication system is working correctly:
- ✅ Token management fixed
- ✅ Authorization headers working
- ✅ Proxy configuration correct
- ✅ Error handling improved
- ✅ User isolation enforced

**Next Steps**: Test additional features (edit task, delete task, toggle completion)
