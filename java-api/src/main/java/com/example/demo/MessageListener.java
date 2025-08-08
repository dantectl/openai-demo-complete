package com.example.demo.listener;

import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class MessageListener {

    @RabbitListener(queues = "ai-response-queue")
    public void receiveMessage(String message) {
        System.out.println("✅ Received AI result from Python: " + message);
        // You could also write this to a database or broadcast to clients here
    }
}
