package com.example.demo.config;

import org.springframework.amqp.rabbit.connection.CachingConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.net.ssl.SSLContext;
import java.security.NoSuchAlgorithmException;

@Configuration
public class RabbitConfig {

    @Bean
    public CachingConnectionFactory rabbitConnectionFactory() throws NoSuchAlgorithmException {
        CachingConnectionFactory factory = new CachingConnectionFactory();
        
        // Set your AWS MQ hostname and port (no scheme prefix)
        factory.setHost("b-f2e4c804-d6cf-41ad-84a1-66c11dd91c1a.mq.us-east-1.on.aws");
        factory.setPort(5671); // TLS port
        factory.setUsername("queueadmin");
        factory.setPassword("r@bbitmQ232!");

        // Enable SSL using default JVM truststore
        factory.getRabbitConnectionFactory().useSslProtocol(SSLContext.getDefault());

        return factory;
    }

    @Bean
    public RabbitTemplate rabbitTemplate(CachingConnectionFactory connectionFactory) {
        return new RabbitTemplate(connectionFactory);
    }
}
