package se.uu.csproject.monadclient;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MotionEvent;
import android.view.View;

import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.util.concurrent.ExecutionException;

import org.apache.commons.validator.routines.EmailValidator;

public class RegisterActivity extends AppCompatActivity {

    private Toolbar toolbar;
    private Button registerButton;
    private EditText username;
    private EditText password;
    private EditText passwordVerify;
    private EditText email;
    private EditText phone;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        registerButton = (Button) findViewById(R.id.button_register);
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
                String emailEntered = email.getText().toString();
                String phoneEntered = phone.getText().toString();

                //check if the fields entered are valid or not
                if(!passwordEntered.equals(passwordVerifyEntered)) {
                    Toast.makeText(getApplicationContext(), "Passwords do not match!",
                            Toast.LENGTH_LONG).show();
                    return;
                }

                if(passwordEntered.length() < 6) {
                    Toast.makeText(getApplicationContext(), "Password must have at least 6 characters!",
                            Toast.LENGTH_LONG).show();
                    return;
                }

                EmailValidator validator = EmailValidator.getInstance();

                if (!validator.isValid(emailEntered)) {
                    Toast.makeText(getApplicationContext(), "Please enter a valid email address!",
                            Toast.LENGTH_LONG).show();
                    return;
                }

                if(!phoneEntered.matches("\\d+")) {
                    Toast.makeText(getApplicationContext(), "Please enter a valid phone number!",
                            Toast.LENGTH_LONG).show();
                    return;
                }

                // initialize a new AsyncTask
                SignUpTask task = new SignUpTask();
                try {
                    // Get the info of the user, send them with the request
                    String response = task.execute(username.getText().toString(), password.getText().toString(), email.getText().toString(), phone.getText().toString()).get();
                    Toast.makeText(getApplicationContext(), response,
                            Toast.LENGTH_LONG).show();
                    // If the user successfully registered, the app will jump to search activity.
                    if (response.startsWith("Success (1)")) {
                        RegisterActivity.this.startActivity(new Intent(RegisterActivity.this, MainActivity.class));
                        finish();
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

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_login, menu);
        return true;
    }
}