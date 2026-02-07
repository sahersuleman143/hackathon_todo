# Quick Test Reference Card

## 🚀 Start Here

1. **Open browser**: http://localhost:3001
2. **Press F12**: Open DevTools → Console tab
3. **Start testing**: Follow the steps below

---

## 🧪 5-Minute Quick Test

### 1️⃣ Register (30 seconds)
- Click "Sign up"
- Email: `test@example.com`
- Password: `password123`
- Click "Sign up"
- ✅ Should redirect to `/dashboard`

### 2️⃣ Create Task (30 seconds)
- Click "Add Task"
- Title: `Buy groceries`
- Description: `Milk, eggs, bread`
- Submit
- ✅ Task appears in list

### 3️⃣ Logout & Login (30 seconds)
- Click "Logout" (top right)
- ✅ Redirected to `/login`
- Login with same credentials
- ✅ Redirected to `/dashboard`
- ✅ Task still visible

### 4️⃣ Session Persistence (1 minute)
- Close entire browser
- Reopen browser
- Go to: http://localhost:3001
- ✅ Automatically logged in
- ✅ Tasks still visible

### 5️⃣ Check Console (1 minute)
Look for these logs:
```
✅ [Auth] Checking authentication...
✅ [API Client] Request: { ... }
✅ [API Client] Response status: 200
✅ [API Client] Success response: { ... }
```

**No red errors!** ❌ If you see errors, check backend logs.

---

## 🎯 Expected Flow

```
http://localhost:3001
        ↓
   Not logged in?
        ↓
   /login page
        ↓
   Sign up/Sign in
        ↓
   /dashboard
        ↓
   Create tasks
        ↓
   View tasks
        ↓
   Logout → /login
```

---

## 🐛 Quick Troubleshooting

### "Failed to fetch"
- Backend down? Check: http://localhost:8000
- Restart: `cd backend && uvicorn src.main:app --reload`

### "Invalid email or password"
- Register first with "Sign up"
- Or use correct credentials

### Tasks don't appear
- Check console for errors
- Check Network tab → `/api/tasks` → Status 200?

### Not redirecting
- Clear browser data (F12 → Application → Clear storage)
- Refresh page (F5)

---

## 📱 Test URLs

| URL | When Logged Out | When Logged In |
|-----|----------------|----------------|
| http://localhost:3001 | → /login | → /dashboard |
| http://localhost:3001/login | Login form | → /dashboard |
| http://localhost:3001/dashboard | → /login | Dashboard page |
| http://localhost:8000/docs | API docs | API docs |

---

## ✅ Success Checklist

- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Can access dashboard when authenticated
- [ ] Can create tasks
- [ ] Tasks persist after page refresh
- [ ] Session persists after closing browser
- [ ] Can logout
- [ ] Cannot access dashboard when logged out
- [ ] Console shows no errors

---

## 🎉 All Tests Pass?

Great! Your full-stack todo app is working correctly.

**Next steps**:
- Test task editing and deletion
- Test with multiple users
- Deploy to production

---

## 📞 Need Help?

Check the detailed guide: `BROWSER_TESTING_GUIDE.md`
