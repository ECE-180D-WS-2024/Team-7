package com.example.chatbot.controller;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Collections;

@RestController
@RequestMapping("/api")
public class ChatController {
    @PostMapping("/chat")
    public ResponseEntity<String> chat(@RequestBody String message) {
        RestTemplate restTemplate = new RestTemplate();
        String url = "https://api.openai.com/v1/chat/completions";

        String apiKey = "Bearer API key";
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
        headers.set("Authorization", apiKey);

        String requestBody = String.format("""
            {
              "model": "gpt-3.5-turbo",
              "messages": [
                {
                  "role": "user",
                  "content": "%s"
                }
              ]
            }
            """, message);

        HttpEntity<String> entity = new HttpEntity<>(requestBody, headers);
        ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.POST, entity, String.class);
        System.out.println("Response Body: " + response.getBody());

        return response;
    }
}
