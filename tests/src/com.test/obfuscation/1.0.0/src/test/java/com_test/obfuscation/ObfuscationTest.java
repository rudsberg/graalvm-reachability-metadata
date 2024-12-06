/*
 * Copyright and related rights waived via CC0
 *
 * You should have received a copy of the CC0 legalcode along with this
 * work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
 */
package com_test.obfuscation;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.fail;
import static org.junit.jupiter.api.Assertions.*;
import org.json.JSONObject;

class ObfuscationTest {
    @Test
    void test() throws Exception {
        System.out.println("Hello from ObfuscationTest. Let's test if org.json was obfuscated...");

        String name = JSONObject.class.getName();
        System.out.println("org.json.JSONObject -> " + name);
    }
}
