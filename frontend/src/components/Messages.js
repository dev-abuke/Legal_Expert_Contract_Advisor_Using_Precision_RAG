import React, { useEffect, useState } from 'react';

const Messages = ({ history }) => {
    const [inputMessage, setInputMessage] = useState("");
    console.log("The history prop is in messages :: ", history);

    const filtered_history = history.filter((item) => item.session_id === "test_ragas");

    // Get the filtered_history of the top 15 messages
    const top_messages = filtered_history.slice(0, 15);

    console.log("The top messages props is :: ", top_messages);

    async function sendMessage(){
        console.log("The input message is :: ", inputMessage);
        const response = await fetch('http://127.0.0.1:8001/qa/from_frontend/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({query: inputMessage}),
        });
        const data = await response.json();
        console.log("The data responded from the Input is :: ", data);
    }

    const getAIMessage = (message, timestamp) => {
        return (
            <div className="flex items-end w-3/4" >
                <img className="w-8 h-8 m-3 rounded-full" src="https://cdn.pixabay.com/photo/2017/01/31/21/23/avatar-2027366_960_720.png" alt="avatar" />
                <div className="p-3 mx-3 dark:bg-gray-800 my-1 rounded-2xl rounded-bl-none max-w-full break-words">
                    <div className="text-xs text-gray-600 dark:text-gray-200">
                        Lizzy
                    </div>
                    <div className="text-gray-700 dark:text-gray-200">
                        {message}
                    </div>
                    <div className="text-xs text-gray-100 dark:text-gray-300 flex justify-end">
                        {timestamp}
                    </div>
                </div>
            </div>
        );
    };

    const getHumanMessage = (message) => {
        return (
            <div className="flex justify-end">
                <div className="flex items-end w-auto bg-purple-500 m-1 rounded-xl rounded-br-none sm:w-3/4 md:w-3/4 max-w-full break-words">
                    <div className="p-2">
                        <div className="text-gray-200 w-auto">
                            {message}
                        </div>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="flex-grow h-full flex flex-col">
            <div className="w-full h-15 p-1 bg-purple-600 dark:bg-gray-800 shadow-md rounded-xl rounded-bl-none rounded-br-none">
                <div className="flex p-2 align-middle items-center">
                    <div className="p-2 md:hidden rounded-full mr-1 hover:bg-purple-500 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                    </div>
                    <div className="border rounded-full border-white p-1/2">
                        <img className="w-14 h-14 rounded-full" src="https://cdn.pixabay.com/photo/2017/01/31/21/23/avatar-2027366_960_720.png" alt="avatar" />
                    </div>
                    <div className="flex-grow p-2">
                        <div className="text-md text-gray-50 font-semibold">Lizzy - Your Legal Assistant </div>
                        <div className="flex items-center">
                            <div className="w-2 h-2 bg-green-300 rounded-full"></div>
                            <div className="text-xs text-gray-50 ml-1">
                                Online
                            </div>
                        </div>
                    </div>
                    <div className="p-2 text-white cursor-pointer hover:bg-purple-500 rounded-full">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                        </svg>
                    </div>
                </div>
            </div>
            <div id='chatWindow' className="w-full flex-grow bg-gray-100 dark:bg-gray-900 my-2 p-2 overflow-y-auto">
                {
                    top_messages.map((message) => {
                        const time = new Date(message.timestamp).toLocaleString("en-US", { hour: "numeric", minute: "numeric", hour12: true });
                        return (
                            <div key={message.id}>
                                {getAIMessage(message.ai_message, time)}
                                {getHumanMessage(message.human_message)}
                            </div>
                        );
                    })
                }
                {/* Here goes the chat history */}
            </div>
            <div className="h-15 p-3 rounded-xl rounded-tr-none rounded-tl-none bg-gray-100 dark:bg-gray-800">
                <div className="flex items-center">
                    <div className="p-2 text-gray-600 dark:text-gray-200 ">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <div className="search-chat flex flex-grow p-2">
                        <input onChange={(e) => setInputMessage(e.target.value)} className="input text-gray-700 dark:text-gray-200 text-sm p-5 focus:outline-none bg-gray-100 dark:bg-gray-800 flex-grow rounded-l-md" type="text" placeholder="Type your message ..." />
                        <div onClick={sendMessage} className="bg-gray-100 dark:bg-gray-800 dark:text-gray-200 flex justify-center items-center pr-3 text-gray-400 rounded-r-md">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Messages;
