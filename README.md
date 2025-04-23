## **Camuflaged - Proof of Concept for Automated Attendance**  

# If you liked it do give it a ⭐

### **⚠️ DISCLAIMER: PROOF OF CONCEPT ONLY**  
Camuflaged is a **proof of concept** project designed to demonstrate that **attendance automation is possible if the underlying algorithm of an attendance system is weak**. This project does not **hack, modify, or manipulate** any official system. Instead, it highlights how a **flawed attendance verification method** can be **exploited by automation**.  

If platforms like **Camu or similar attendance systems** want to maintain security, they **should improve their algorithm and implement better verification methods** to prevent easy automation.  

This project is made **for educational and research purposes only**. By using or deploying it, **you acknowledge all risks involved**.  

---

## **📌 How to Use (Self-Host & Automate Attendance)**  
### **1️⃣ Clone the Repository**  
- Clone this repo to your GitHub.  
- **Keep the repo private** to protect stored user data.  

### **2️⃣ Change Admin Credentials**  
- Modify the **admin username and password** (highly recommended).  
- The admin will have access to all user data and full control over the system.  

### **3️⃣ Deploy to Railway.app**  
- **Create an account** on [Railway.app](https://railway.app/) (free hosting).  
- Use the provided **Dockerfile** to deploy the repo directly.  
- Follow Railway's instructions to **connect your service to the web**.  

### **4️⃣ How It Works (Once Deployed)**  
✅ Admin must login and click on "Start Loop" for auto attendace marking on qr generation for registered users.
                                       OR
✅ Any registered user can **sign in and mark attendance** for **everyone in the same batch/group**.  
✅ New users can **register** and need not to register again lest admin forget to save and update the latest database .  
✅ As long as **one user scans attendance, all others in that batch are marked present**.  
✅ **Fully automated process**—no manual marking needed after setup.  

---

## **⚠️ IMPORTANT NOTES**  
🔴 **Admin Control** → **Be sure to personally know the admin** because they have full access to all stored user data.  
🔴 **Database Persistence** → **Every time the admin restarts the service on Railway, the database is wiped.** Before restarting, follow these steps:
   - **Login as Admin → Go to Files → Search for `database.db` → Download and save locally**.  
   - Add it back to the repo before restarting.  

🔴 **UI is Incomplete** → Some parts of the UI are unfinished because **I lost interest in this project**. There might be **no to very few future updates**.  

🔴 **Use at Your Own Risk** → Any **user registering or using this service takes full responsibility for any consequences**. The creator holds **zero liability**.  

---

## **👀 WHY ARE YOU HERE?**  
🚨 **You are here because you want this.** This project is publicly available, and **no one is forcing you to use it**. If you deploy and use it, it’s **100% your decision and responsibility**.  

---

### **🛠️ Anything More?** 

> *“If you don’t understand how to manage databases, secure credentials, or deploy web apps, you probably shouldn’t be running this.”* 
