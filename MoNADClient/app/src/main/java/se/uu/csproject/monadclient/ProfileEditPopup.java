package se.uu.csproject.monadclient;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.InputType;
import android.util.DisplayMetrics;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.concurrent.ExecutionException;


public class ProfileEditPopup extends AppCompatActivity {
    private Button button_editprofile_cancel;
    private Button button_editprofile_ok;
    private TextView textview_editprofile_name;
    private EditText edittext_editprofile_textfield;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_profile_edit);

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int) (width * .9), (int) (height * .33));

        Intent intent = getIntent();
        final String name = intent.getStringExtra("name");
        changeProfileText(name);

        button_editprofile_ok = (Button)findViewById(R.id.button_editprofile_btnok);
        button_editprofile_ok.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                UpdateProfileTask task = new UpdateProfileTask();
                try {
                    // Get the username and password, send them with the request
                    String clientid = ClientAuthentication.getClientId();
                    String username = ClientAuthentication.getUsername();
                    String password = ClientAuthentication.getPassword();
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
                    String response = task.execute(clientid, username, password, email, phone).get();
                    Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();
                    // If the reponse starts with the specific word, it means the user updated the profile successfully
                    if (response.startsWith("Success (1)")) {
                        startActivity(new Intent(ProfileEditPopup.this, ProfileActivity.class));
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (ExecutionException e) {
                    e.printStackTrace();
                }
            }
        });

        button_editprofile_cancel = (Button)findViewById(R.id.button_editprofile_btncancel);
        button_editprofile_cancel.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                finish();
            }
        });

    }

    public void changeProfileText(String name){
        //handles textview and textfield changes and
        // set values on changing profile text
        textview_editprofile_name = (TextView)findViewById(R.id.textview_editprofile_textfieldname);
        edittext_editprofile_textfield = (EditText)findViewById(R.id.edittext_editprofile_editfield);
        if(name.equals("username")){
            textview_editprofile_name.setText("Username :");
            edittext_editprofile_textfield.setInputType(InputType.TYPE_CLASS_TEXT);
        }
        if(name.equals("phone")){
            textview_editprofile_name.setText("Phone No. :");
            edittext_editprofile_textfield.setInputType(InputType.TYPE_CLASS_PHONE);
        }
        if(name.equals("email")){
            textview_editprofile_name.setText("Email :");
            edittext_editprofile_textfield.setInputType(InputType.TYPE_TEXT_VARIATION_WEB_EMAIL_ADDRESS);
        }
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
