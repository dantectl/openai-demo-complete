package com.example.demo.model;

public class MyRequestPayload {
    private String name;
    private int age;
    private String number;

    public MyRequestPayload() {
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getNumber() {
        return number;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    @Override
    public String toString() {
        return "MyRequestPayload{name='" + name + "', age=" + age + ", number='" + number + "'}";
    }
}
