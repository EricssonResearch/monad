package se.uu.csproject.monadclient.activities;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.MotionEvent;
import android.view.View;

import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.util.concurrent.ExecutionException;

import se.uu.csproject.monadclient.R;
import se.uu.csproject.monadclient.SignUpTask;

public class RegisterActivity extends AppCompatActivity {

    private EditText username;
    private EditText password;
    private EditText passwordVerify;
    private EditText email;
    private EditText phone;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        Toolbar toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        Button registerButton = (Button) findViewById(R.id.button_register);
        username = (EditText) findViewById(R.id.field_username);
        password = (EditText) findViewById(R.id.field_password);
        passwordVerify = (EditText) findViewById(R.id.field_verify_password);
        email = (EditText) findViewById(R.id.field_email);
        phone = (EditText) findViewById(R.id.field_phone);

        registerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String passwordEntered = password.getText().toString();
                String passwordVerifyEntered = passwordVerify.getText().toString();

                //check if the two passwords match or not
                if (!passwordEntered.equals(passwordVerifyEntered)) {
                    Toast.makeText(getApplicationContext(), getString(R.string.java_passwordsnomatch),
                            Toast.LENGTH_LONG).show();
                    return;
                }

                // initialize a new AsyncTask
                SignUpTask task = new SignUpTask();
                try {
                    // Get the info of the user, send them with the request
                    String response = task.execute(username.getText().toString(), passwordEntered, email.getText().toString(), phone.getText().toString()).get();
                    // If the user successfully registered, the app will jump to search activity.
                    if (response.startsWith("Success (1)")) {
                        Toast.makeText(getApplicationContext(), getString(R.string.java_signupsuccess), Toast.LENGTH_LONG).show();
                        RegisterActivity.this.startActivity(new Intent(RegisterActivity.this, MainActivity.class));
                        setResult(RESULT_OK);
                        finish();
                    } else {
                        Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (ExecutionException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    // hides the phone keyboard when an element is touched besides the keyboard and text fields
    public boolean onTouchEvent(MotionEvent event) {
        InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
        return true;
    }
}