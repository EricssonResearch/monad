package se.uu.csproject.monadclient;

import android.content.Intent;
import android.media.Image;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import java.util.concurrent.ExecutionException;


public class ProfileActivity extends MenuedActivity {

    Toolbar toolbar;
    Button submitButton;
    ImageButton passwordButton;
    private EditText usernameField;
    private EditText emailField;
    private EditText phoneField;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);
        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        //set the profile fields from the profile stored in ClientAuthentication
        usernameField = (EditText)findViewById(R.id.textView_profile_user);
        usernameField.setText(ClientAuthentication.getUsername());

        phoneField = (EditText)findViewById(R.id.textView_profile_phone);
        phoneField.setText(ClientAuthentication.getPhone());

        emailField = (EditText)findViewById(R.id.textView_profile_email);
        emailField.setText(ClientAuthentication.getEmail());

        submitButton = (Button) findViewById(R.id.button_updateprofile);
        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                editProfileInfo(v);
            }
        });

        passwordButton = (ImageButton) findViewById(R.id.button_changepassword);
        passwordButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                changePassword(v);
            }
        });
    }

    public void changePassword(View v){
        Intent intent = new Intent(this, ResetPasswordActivity.class);
        intent.putExtra("RESET", false); //to determine how to display the ResetPasswordActivity
        startActivityForResult(intent, 1);
    }

//    @Override
//    public boolean onCreateOptionsMenu(Menu menu) {
//        // Inflate the menu; this adds items to the action bar if it is present.
//        getMenuInflater().inflate(R.menu.menu_main, menu);
//        return true;
//    }
//
//    @Override
//    public boolean onOptionsItemSelected(MenuItem item) {
//        // Handle action bar item clicks here. The action bar will
//        // automatically handle clicks on the Home/Up button, so long
//        // as you specify a parent activity in AndroidManifest.xml.
//        int id = item.getItemId();
//
//        if(id == android.R.id.home) {
//            NavUtils.navigateUpFromSameTask(this);
//        }
//
//        if (id == R.id.action_search) {
//            startActivity(new Intent(this, MainActivity.class));
//        }
//
//        if (id == R.id.action_notifications) {
//            startActivity(new Intent(this, NotificationsActivity.class));
//        }
//
//        if (id == R.id.action_mytrips) {
//            startActivity(new Intent(this, TripsActivity.class));
//        }
//
//        if (id == R.id.action_profile) {
//            return true;
//        }
//
//        //noinspection SimplifiableIfStatement
//        if (id == R.id.action_settings) {
//            startActivity(new Intent(this, SettingsActivity.class));
//        }
//
//        if (id == R.id.action_aboutus) {
//            //TODO (low priority): Create a toaster with text about the MoNAD project and team
//            startActivity(new Intent(this, AboutUsActivity.class));
//        }
//
//        if (id == R.id.action_signout) {
//            startActivity(new Intent(this, LoginActivity.class));
//        }
//
//        return super.onOptionsItemSelected(item);
//    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if(id == R.id.action_profile){
            return true;
        }
        else {
            return super.onOptionsItemSelected(item);
        }
    }

    public void editProfileInfo(View v){
        String userEntered = usernameField.getText().toString();
        String emailEntered = emailField.getText().toString();
        String phoneEntered = phoneField.getText().toString();

        if(!phoneEntered.matches("\\d+")) {
            Toast.makeText(getApplicationContext(), "Please enter a valid phone number!",
                    Toast.LENGTH_LONG).show();
            return;
        }

        UpdateProfileTask task = new UpdateProfileTask();

        String response = null;
        try {
            response = task.execute(ClientAuthentication.getClientId(), userEntered, emailEntered, phoneEntered).get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();

        if(response.startsWith("Success (1)")){
            usernameField.setText(ClientAuthentication.getUsername());
            emailField.setText(ClientAuthentication.getEmail());
            phoneField.setText(ClientAuthentication.getPhone());
        }
        /*UpdateProfileTask task = new UpdateProfileTask();
        try {
            String clientid = ClientAuthentication.getClientId();
            String username = ClientAuthentication.getUsername();
            String email = ClientAuthentication.getEmail();
            String phone = ClientAuthentication.getPhone();

            edittext_editprofile_textfield = (EditText)findViewById(R.id.edittext_editprofile_editfield);
            String input = edittext_editprofile_textfield.getText().toString();

            if(name.equals("username")){
                username = input;
            }
            else if(name.equals("phone")){
                phone = input;
            }
            else if(name.equals("email")){
                email = input;
            }
            String response = task.execute(clientid, username, email, phone).get();
            Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();
            // If the reponse starts with the specific word, it means the user updated the profile successfully
            if (response.startsWith("Success (1)")) {
                startActivity(new Intent(ProfileEditPopup.this, ProfileActivity.class));
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }*/
    }
}