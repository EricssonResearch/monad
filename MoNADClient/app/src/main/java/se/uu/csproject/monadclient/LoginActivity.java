package se.uu.csproject.monadclient;

import android.content.Context;
import android.content.Intent;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;

import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.common.SignInButton;

import java.util.concurrent.ExecutionException;

public class LoginActivity extends AppCompatActivity {

    private EditText usernameField;
    private EditText passwordField;
    private SignInButton googleLogInButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Toolbar toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        usernameField = (EditText) findViewById(R.id.field_username);
        passwordField = (EditText) findViewById(R.id.field_password);
        Button logInButton = (Button) findViewById(R.id.button_login);
        TextView forgotPasswordTextView = (TextView) findViewById(R.id.forgotpassword_text_view);
        TextView registerTextView = (TextView) findViewById(R.id.textview_register);
        googleLogInButton = (SignInButton) findViewById(R.id.google_login_button);

        googleLogInButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LoginActivity.this.startActivity(new Intent(LoginActivity.this, GoogleLogIn.class));
            }
        });

        logInButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LogInTask task = new LogInTask();
                try {
                    // Get the username and password, send them with the request
                    String response = task.execute(usernameField.getText().toString(), passwordField.getText().toString()).get();
                    Toast.makeText(getApplicationContext(), response,
                            Toast.LENGTH_LONG).show();
                    // If the reponse starts with the specific word, it means the users loged in successfully
                    if (response.startsWith("Success (1)")) {
                        LoginActivity.this.startActivity(new Intent(LoginActivity.this, MainActivity.class));
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (ExecutionException e) {
                    e.printStackTrace();
                }
            }
        });

        forgotPasswordTextView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LoginActivity.this.startActivity(new Intent(v.getContext(), ForgotPasswordPopup.class));
            }
        });

        registerTextView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LoginActivity.this.startActivity(new Intent(v.getContext(), RegisterActivity.class));
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_login, menu);
        return true;
    }

    // hides the phone keyboard when an element is touched besides the keyboard and text fields
    public boolean onTouchEvent(MotionEvent event) {
        InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if(id == android.R.id.home){
            NavUtils.navigateUpFromSameTask(this);
        }

        if (id == R.id.action_search) {
            startActivity(new Intent(this, MainActivity.class));
        }

        if (id == R.id.action_notifications) {
            startActivity(new Intent(this, NotificationsActivity.class));
        }

        if (id == R.id.action_mytrips) {
            startActivity(new Intent(this, TripsActivity.class));
        }

        if (id == R.id.action_profile) {
            startActivity(new Intent(this, ProfileActivity.class));
        }

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            startActivity(new Intent(this, SettingsActivity.class));
        }

        if (id == R.id.action_aboutus) {
            startActivity(new Intent(this, AboutUsActivity.class));
        }

        if (id == R.id.action_signout) {
            startActivity(new Intent(this, LoginActivity.class));
        }

        return super.onOptionsItemSelected(item);
    }
}
