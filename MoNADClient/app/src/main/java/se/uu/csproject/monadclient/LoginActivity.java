package se.uu.csproject.monadclient;

import android.content.Context;
import android.content.Intent;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.DisplayMetrics;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;

import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.google.android.gms.common.SignInButton;

public class LoginActivity extends AppCompatActivity {

    private Toolbar toolbar;
    private EditText usernameField;
    private EditText passwordField;
    private Button logInButton;
    private TextView wrongCredentials;
    private TextView registerTextView;
    private TextView forgotPasswordTextView;

    //added by functionality team
    private SignInButton googleSignInButton;
    //added by functionality team

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        usernameField = (EditText) findViewById(R.id.field_username);
        passwordField = (EditText) findViewById(R.id.field_password);
        logInButton = (Button) findViewById(R.id.button_login);
        wrongCredentials = (TextView) findViewById(R.id.wrong_credentials);
        forgotPasswordTextView = (TextView) findViewById(R.id.forgotpassword_text_view);
        registerTextView = (TextView) findViewById(R.id.textview_register);

        //added by functionality team
        googleSignInButton = (SignInButton) findViewById(R.id.google_login_button);

        googleSignInButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LoginActivity.this.startActivity(new Intent(LoginActivity.this, GoogleLogIn.class));
            }
        });
        //added by functionality team

        logInButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (usernameField.getText().toString().equals("monad")
                        && passwordField.getText().toString().equals("monad")) {
                    LoginActivity.this.startActivity(new Intent(LoginActivity.this, MainActivity.class));
                } else {
                    wrongCredentials.setVisibility(TextView.VISIBLE);
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

        if (id == android.R.id.home) {
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
