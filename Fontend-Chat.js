document.addEventListener('DOMContentLoaded', () => { 
    const chatbotContainer = document.querySelector('.chatbot-container');

    // สร้างองค์ประกอบภายใน chatbotContainer
    chatbotContainer.innerHTML = `
        <button class="close-chat">ปิด</button>
        <div class="chat-messages"></div>
        <div class="chat-input">
            <input type="text" placeholder="พิมพ์ที่นี่">
            <button class="send-button">ส่ง</button>
        </div>
    `;

    const chatToggle = document.querySelector('.chat-toggle');
    const closeChat = document.querySelector('.close-chat');
    const chatMessages = document.querySelector('.chat-messages');
    const chatInput = document.querySelector('.chat-input input');
    const sendButton = document.querySelector('.chat-input button');

    // เปิด-ปิดหน้าต่างแชท
    chatToggle.addEventListener('click', () => {
        chatbotContainer.style.display = chatbotContainer.style.display === 'none' ? 'block' : 'none';
    });
    document.addEventListener('DOMContentLoaded', () => { 
        const chatbotContainer = document.querySelector('.chatbot-container');
    
        // สร้างองค์ประกอบภายใน chatbotContainer
        chatbotContainer.innerHTML = `
            <button class="close-chat">ปิด</button>
            <div class="chat-messages"></div>
            <div class="chat-input">
                <input type="text" placeholder="พิมพ์ที่นี่">
                <button class="send-button">ส่ง</button>
            </div>
        `;
    
        const chatToggle = document.querySelector('.chat-toggle');
        const closeChat = document.querySelector('.close-chat');
        const chatMessages = document.querySelector('.chat-messages');
        const chatInput = document.querySelector('.chat-input input');
        const sendButton = document.querySelector('.chat-input button');
    
        // เปิด-ปิดหน้าต่างแชท
        chatToggle.addEventListener('click', () => {
            chatbotContainer.style.display = chatbotContainer.style.display === 'none' ? 'block' : 'none';
        });
    
        // ปิดแชท
        closeChat.addEventListener('click', () => {
            chatbotContainer.style.display = 'none';
        });
    
        // ส่งข้อความไปยัง API
        const sendMessage = async () => {
            const userMessage = chatInput.value;
            if (userMessage.trim() === '') return;
    
            // แสดงข้อความของผู้ใช้
            displayMessage(userMessage, 'user-message');
            chatInput.value = '';
    
            try {
                const response = await fetch('http://127.0.0.1:5000/Chatbot-bankok', { 
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ inputText: userMessage }),
                });
    
                if (!response.ok) {
                    throw new Error('Error in API response');
                }
    
                const data = await response.json();
                displayMessage(data.reply, 'bot-message');
            } catch (error) {
                console.error('ข้อผิดพลาด:', error);
                displayMessage('ขอโทษค่ะ มีข้อผิดพลาดเกิดขึ้น กรุณาลองใหม่อีกครั้ง', 'bot-message');
            }
        };
    
        // ฟังก์ชันเพื่อแสดงข้อความในหน้าต่างแชท
        function displayMessage(message, className) {
            const messageElement = document.createElement('div');
            messageElement.textContent = message;
            messageElement.className = className; // กำหนดคลาสตามประเภทข้อความ
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight; // เลื่อนอัตโนมัติไปที่ข้อความล่าสุด
        }
    
        // ส่งข้อความเมื่อกดปุ่มหรือ Enter
        sendButton.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    });
    function displayMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        messageElement.className = className; // กำหนดคลาสตามประเภทข้อความ
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // เลื่อนอัตโนมัติไปที่ข้อความล่าสุด
    }
    
    // ปิดแชท
    closeChat.addEventListener('click', () => {
        chatbotContainer.style.display = 'none';
    });

    // ส่งข้อความไปยัง API
    const sendMessage = async () => {
        const userMessage = chatInput.value;
        if (userMessage.trim() === '') return;

        // แสดงข้อความของผู้ใช้
        displayMessage(userMessage, 'user-message');
        chatInput.value = '';

        try {
            const response = await fetch('http://127.0.0.1:5000/Chatbot-bankok', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ inputText: userMessage }),
            });

            if (!response.ok) {
                throw new Error('Error in API response');
            }

            const data = await response.json();
            displayMessage(data.reply, 'bot-message');
        } catch (error) {
            console.error('ข้อผิดพลาด:', error);
            displayMessage('ขอโทษค่ะ มีข้อผิดพลาดเกิดขึ้น กรุณาลองใหม่อีกครั้ง', 'bot-message');
        }
    };

    // ฟังก์ชันเพื่อแสดงข้อความในหน้าต่างแชท
    function displayMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        messageElement.className = className; // กำหนดคลาสตามประเภทข้อความ
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // เลื่อนอัตโนมัติไปที่ข้อความล่าสุด
    }

    // ส่งข้อความเมื่อกดปุ่มหรือ Enter
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
