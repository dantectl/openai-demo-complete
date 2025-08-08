package com.example.demo.controller;

import com.example.demo.model.MyRequestPayload;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;


@RestController
@CrossOrigin(origins = "http://localhost:8088")
public class UserController {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    private static final String QUEUE_NAME = "userdetails";

    @PostMapping("/api/process")
    public ResponseEntity<String> processData(@RequestBody MyRequestPayload payload) throws JsonProcessingException {
        ObjectMapper mapper = new ObjectMapper();
        String jsonPayload = mapper.writeValueAsString(payload);
        System.out.println("Received data: " + payload);

        // Convert the payload to a string or JSON (Spring will do it automatically if Jackson is present)
        rabbitTemplate.convertAndSend("userdetails", jsonPayload);

      //  rabbitTemplate.convertAndSend("", QUEUE_NAME, payload.toString());

        System.out.println("Message sent to RabbitMQ queue: " + QUEUE_NAME);

        // Return response
        String result = "Submitted";
        return ResponseEntity.ok(result);
    }
}
