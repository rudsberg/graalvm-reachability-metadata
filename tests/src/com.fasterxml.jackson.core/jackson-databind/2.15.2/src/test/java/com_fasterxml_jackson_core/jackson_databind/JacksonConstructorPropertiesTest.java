/*
 * Copyright and related rights waived via CC0
 *
 * You should have received a copy of the CC0 legalcode along with this
 * work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
 */
package com_fasterxml_jackson_core.jackson_databind;

// import java.beans.ConstructorProperties;

// import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

// import static org.assertj.core.api.Assertions.assertThat;

class JacksonConstructorPropertiesTest {

    static final ObjectMapper mapper;

    static {
        System.out.println("Initializing ObjectMapper");
        mapper = new ObjectMapper();
        System.out.println("ObjectMapper initialized");
    }

    @Test
    void deserializeConstructorProperties() { // throws JsonProcessingException
        System.out.println("hello");
        // System.out.println("com_fasterxml_jackson_core.jackson_databind.Foo -> " + Foo.class.getName());
        // Foo foo = mapper.readValue("{ \"bar\": \"baz\" }", Foo.class);
        // assertThat(foo.getBar()).isEqualTo("baz");
    }

    // static class Foo {

    //     private String bar;

    //     @ConstructorProperties("bar")
    //     Foo(String bar) {
    //         this.bar = bar;
    //     }

    //     String getBar() {
    //         return bar;
    //     }
    // }

}
