# 🛍️ Virtual Shopping Assistant

## 📌 Overview
This repository contains an AI-powered **Virtual Shopping Assistant** built using **LangChain + Ollama (Mistral LLM)**. The assistant integrates **multiple e-commerce tools** to help users with product searches, price comparisons, shipping estimates, promo code validation, and return policy checks.

---

## 📊 Comparative Conceptual Map (Analysis of Approaches)

| **Approach** | **Concept** | **Advantages** | **Disadvantages** | **Use Case Suitability** |
|-------------|------------|---------------|------------------|--------------------|
| **1. LangChain + Ollama (Agentic AI)** | Uses **Ollama LLM** (`mistral`) with **LangChain's Agent framework**, integrating multiple tools. | ✅ **Modular & Extensible** <br> ✅ **Context-aware multi-turn reasoning** <br> ✅ **Auto-tool selection** | ❌ **Increased latency due to multiple function calls** <br> ❌ **Moderate compute cost** | 🛍️ **E-commerce shopping assistant** <br> 🛒 **Multi-step queries** |
| **2. Rule-Based Chatbot** | Uses predefined **if-else conditions** for responses. | ✅ **Fast & reliable** <br> ✅ **Low compute cost** | ❌ **Lacks adaptability & reasoning** <br> ❌ **Fails in non-predefined cases** | 📞 **Basic Q&A for customer service** |
| **3. LLM-Based RAG (Retrieval-Augmented Generation)** | Fetches real-time product info via **vector search** + LLM. | ✅ **Highly accurate with real-time data** <br> ✅ **Fewer hallucinations** | ❌ **Slower than API-based approaches** <br> ❌ **Requires vector DB infrastructure** | 🔎 **Product search & fashion trend analysis** |
| **4. API-Driven AI Assistant** | Uses **prebuilt APIs** for fetching shopping data **without LLM-based reasoning**. | ✅ **Fast & cost-effective** <br> ✅ **Accurate data fetching** | ❌ **Limited reasoning ability** <br> ❌ **API constraints affect flexibility** | 📦 **Real-time product lookup** |
| **5. Fine-Tuned LLM for Shopping** | Trained on **domain-specific** shopping data. | ✅ **Highly optimized for shopping** <br> ✅ **No external API reliance** | ❌ **Expensive to train & maintain** <br> ❌ **Lacks real-time adaptability** | 🧵 **Personalized shopping assistants** |

---

## 📄 Short Written Analysis (Results & Performance)

1. **LangChain + Ollama (Agentic AI) 🏆**
   - ✅ **Best for dynamic, multi-turn reasoning** and tool-based execution.
   - ✅ **Handles complex queries** (e.g., price comparison, shipping estimates).
   - ❌ **Moderate latency** due to LLM inference + tool execution.

2. **Rule-Based Chatbot**
   - ✅ **Fastest response time**, highly efficient.
   - ❌ **Lacks reasoning**, fails for non-predefined queries.

3. **LLM-Based RAG (Retrieval-Augmented Generation)**
   - ✅ **Most accurate for real-time product search**.
   - ❌ **Slower due to retrieval + LLM processing**.

4. **API-Driven AI Assistant**
   - ✅ **Fastest, cost-efficient for real-time price checks**.
   - ❌ **Cannot handle reasoning or multi-step queries**.

5. **Fine-Tuned Custom LLM**
   - ✅ **Best for domain-optimized responses**.
   - ❌ **Expensive training & lacks real-time adaptability**.

🔹 **For multi-step shopping assistance, LangChain + Ollama is the best choice**. 🚀

---

## 🎯 Design Decisions (Agent Architecture & Tool Selection)

### **1️⃣ Agent Architecture: Why LangChain + Ollama?**
✅ **Agentic AI Approach:**
- Uses **LangChain's OpenAI-style agent**, dynamically invoking tools based on user queries.
- Enables **multi-turn conversations** with memory retention.

✅ **LLM Selection: Ollama (Mistral)**
- **Lightweight & efficient**.
- **Supports on-device/local deployment**.
- **Balanced creativity & accuracy (temperature = 0.7).**

✅ **Memory: ConversationBufferMemory**
- Stores chat history for context-aware interactions.

### **2️⃣ Tool Selection**

| **Tool Name** | **Function** | **Purpose** |
|--------------|-------------|------------|
| **SearchProducts** | `search_products()` | Fetches product listings from e-commerce websites. |
| **EstimateShipping** | `estimate_shipping()` | Provides shipping costs & delivery estimates. |
| **CheckPromoCode** | `check_promo()` | Validates promo codes & calculates discounts. |
| **ComparePrices** | `compare_prices()` | Compares prices across stores. |
| **GetReturnPolicy** | `get_return_policy()` | Retrieves store return policies. |

🔹 **Tool-based execution ensures real-time accuracy & efficiency**. 🚀

---

## **📄 How to Set Up the Project**

### **1️⃣ Create a Virtual Environment**
```sh
python3 -m venv localenv
source localenv/bin/activate  # On macOS/Linux
localenv\Scripts\activate    # On Windows
```

### **2️⃣ Install Ollama**
```sh
curl -fsSL https://ollama.com/install.sh | sh
```

### **3️⃣ Pull the Mistral Model from Ollama**
```sh
ollama pull mistral
```

### **4️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **5️⃣ Run the Shopping Agent**
```sh
python3 agent.py
```

### **1️⃣ Deployment link of the project**
```sh
https://0b9b-2402-e280-230d-37b-5cae-dd4a-9f37-620.ngrok-free.app/
```


🔹 **Ask the Fashion products related question**. 🚀




--- 

## 🚧 Challenges & Improvements

### **Challenges Faced**
❌ **Latency in Tool Execution:** Calling multiple APIs slows down responses.  
❌ **Handling Edge Cases:** Unexpected queries not covered in the initial training.  
❌ **LLM Hallucinations:** Sometimes generates incorrect or made-up product details.  

### **Potential Improvements**
✅ **Parallel API Calls**: Optimize function execution for speed.  
✅ **Better Query Parsing**: Pre-process user input for better tool selection.  
✅ **Hybrid Approach (LLM + RAG)**: Implement retrieval-based knowledge grounding.  

---

## ❓ Open Questions & References

### **Open Questions**
- How can we further **reduce API latency** while maintaining accuracy?
- Should we **fine-tune a custom LLM** to reduce reliance on API calls?
- What is the best way to **handle conflicting product data** from different stores?

### **References**
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama LLM Models](https://ollama.ai/)
- [Retrieval-Augmented Generation (RAG) Research](https://arxiv.org/abs/2005.11401)
- [Best Practices in AI-Powered Shopping Assistants](https://arxiv.org/abs/2301.00892)

---

🔹 **This repository is actively maintained**. Contributions are welcome! 🚀
