import React from 'react'
import ConversationItem from './ConversationItem';

const Conversation = ({conversation}) => {
    console.log("The conversation from prop is :: ", conversation)

    return (
        <div className="p-1">
            {
                conversation?.map((item, index) => (
                    <ConversationItem
                        key={index}
                        message={item.message}
                        time={item.time} 
                        name={item.name} 
                        active={item.active}
                    />
                ))
            }
        </div>
    )
}

export default Conversation
