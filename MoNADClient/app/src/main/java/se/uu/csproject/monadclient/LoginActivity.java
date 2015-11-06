package se.uu.csproject.monadclient;

import android.content.Context;
import android.content.Intent;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;

import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.common.SignInButton;

import java.util.concurrent.ExecutionException;

import se.uu.csproject.monadclient.googlecloudmessaging.RegistrationIntentService;

public class LoginActivity extends AppCompatActivity {
    private final int GOOGLE_LOGIN_REQUEST = 1;
    private final int REGISTER_REQUEST = 2;

    private EditText usernameField;
    private EditText passwordField;
    private SignInButton googleLogInButton;
    private TextView wrongCredentialsTextView;

    //Google Cloud Services
    private static final String TAG = "MainActivity";
    private static final int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Toolbar toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        if (checkPlayServices()) {
            Intent intent = new Intent(this,RegistrationIntentService.class);
            startService(intent);

        }

        usernameField = (EditText) findViewById(R.id.field_username);
        passwordField = (EditText) findViewById(R.id.field_password);
        Button logInButton = (Button) findViewById(R.id.button_login);
        TextView forgotPasswordTextView = (TextView) findViewById(R.id.forgotpassword_text_view);
        TextView registerTextView = (TextView) findViewById(R.id.textview_register);
        wrongCredentialsTextView = (TextView) findViewById(R.id.wrong_credentials);
        googleLogInButton = (SignInButton) findViewById(R.id.google_login_button);

        googleLogInButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LoginActivity.this.startActivityForResult(new Intent(LoginActivity.this, GoogleLogIn.class), GOOGLE_LOGIN_REQUEST);
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
                    // If the response starts with the specific word, it means the users logged in successfully
                    if (response.startsWith("Success (1)")) {
                        LoginActivity.this.startActivity(new Intent(LoginActivity.this, MainActivity.class));
                        finish();
                    }
                    else if (response.startsWith("Wrong Credentials (0)")) {
                        wrongCredentialsTextView.setVisibility(View.VISIBLE);
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
                LoginActivity.this.startActivityForResult((new Intent(LoginActivity.this, RegisterActivity.class)), REGISTER_REQUEST);
            }
        });
    }

    /* if google login/register succeeds, then the login activity is destroyed
     * a user cannot go back to login back if he/she is already logged in
     * the user can only sign out and then he/she will be shown the login layout again
     */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if((requestCode == GOOGLE_LOGIN_REQUEST || requestCode == REGISTER_REQUEST) && resultCode == RESULT_OK){
            finish();
        }
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

    private boolean checkPlayServices() {

        GoogleApiAvailability apiAvailability = GoogleApiAvailability.getInstance();
        int resultCode = apiAvailability.isGooglePlayServicesAvailable(this);
        if (resultCode != ConnectionResult.SUCCESS) {
            if (apiAvailability.isUserResolvableError(resultCode)) {
                apiAvailability.getErrorDialog(this, resultCode, PLAY_SERVICES_RESOLUTION_REQUEST)
                        .show();
            } else {
                Log.i(TAG, "This device is not supported.");
                finish();
            }
            return false;
        }
        return true;
    }
}
