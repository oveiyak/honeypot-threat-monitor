package com.example.honeypot_test;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import java.io.IOException;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "HoneypotTest";
    private static final String BASE_URL = "http://10.0.2.2:5000"; // Android emulator localhost
    private TextView resultTextView;
    private OkHttpClient client;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        resultTextView = findViewById(R.id.resultTextView);
        client = new OkHttpClient();

        // Test vulnerable endpoints
        testAdminLogin();
        testUserData();
        testConfig();
    }

    private void testAdminLogin() {
        JSONObject loginData = new JSONObject();
        try {
            loginData.put("username", "admin");
            loginData.put("password", "password123");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        Request request = new Request.Builder()
                .url(BASE_URL + "/api/v1/admin/login")
                .post(okhttp3.RequestBody.create(loginData.toString(), okhttp3.MediaType.parse("application/json")))
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e(TAG, "Admin login failed", e);
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                final String responseData = response.body().string();
                runOnUiThread(() -> resultTextView.append("\nAdmin Login Response: " + responseData));
            }
        });
    }

    private void testUserData() {
        Request request = new Request.Builder()
                .url(BASE_URL + "/api/v1/users/data")
                .get()
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e(TAG, "User data fetch failed", e);
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                final String responseData = response.body().string();
                runOnUiThread(() -> resultTextView.append("\nUser Data Response: " + responseData));
            }
        });
    }

    private void testConfig() {
        Request request = new Request.Builder()
                .url(BASE_URL + "/api/v1/config")
                .get()
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e(TAG, "Config fetch failed", e);
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                final String responseData = response.body().string();
                runOnUiThread(() -> resultTextView.append("\nConfig Response: " + responseData));
            }
        });
    }
} 