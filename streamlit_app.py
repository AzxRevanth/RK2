import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("RK SIR STUDENTS")
st.markdown("DATA ENTRY")

# Establishing a Google Sheets connection
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Fetch existing students data
existing_data = conn.read(worksheet="Sheet1", usecols=list(range(7)), ttl=5)
existing_data = existing_data.dropna(how="all")

# Choose an Action
action = st.selectbox(
    "Choose an Action",
    [
        "DATA VIEWING",
        "DATA ENTRY",
        "UPDATE EXISTING ENTRY",
        "DELETE ENTRY",
        "FEES DUE NEXT MONTH",
    ],
)

# Based on the selected action, display the relevant information
if action == "DATA VIEWING":
    # Display the original data again
    st.header('DATA VIEWING')
    st.dataframe(existing_data)

    # Ensure 'Date of Joining' is treated as datetime
    existing_data['Date of Joining'] = pd.to_datetime(existing_data['Date of Joining'])

    # Calculate the fee due date (next month from the date of joining)
    existing_data['Fee Due Date'] = existing_data['Date of Joining'] + pd.offsets.MonthBegin(1)

    # Filter students with fees due in the next month
    due_date_filter = (existing_data['Fee Due Date'] >= pd.Timestamp.today()) & (
        existing_data['Fee Due Date'] <= pd.Timestamp.today() + pd.DateOffset(days=3)
    )
    due_students_df = existing_data[due_date_filter]

    if due_students_df.empty:
        st.info("No students have fees due in the next month.")
    else:
        st.dataframe(
            due_students_df[['Student Name', 'Grade', 'Date of Joining', 'Subject', 'Fees', 'Amount Paid', 'Fee Due Date']]
        )

elif action == "DATA ENTRY":
    # Take input for new data
    st.subheader('Enter New Data')

    # Use st.form() to wrap the form elements
    with st.form(key='my_form'):
        AdminNo = st.text_input('Admission Number*')
        student_name = st.text_input('Student Name*')
        grade = st.text_input('Grade*')
        date_of_joining = st.date_input('Date of Joining*')
        subject = st.text_input('Subject*')
        fees = st.number_input('Fees*')
        amount_paid = st.number_input('Amount Paid*')

        # Mark mandatory fields
        st.markdown("**required*")

        # st.form_submit_button should be used inside the st.form() context
        submit_button = st.form_submit_button(label="Submit Students Details")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not AdminNo or not student_name or not grade or not date_of_joining or not subject or not fees or not amount_paid:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()

        # Convert "Student Name" column to string for checking duplicates
        existing_data["Student Name"] = existing_data["Student Name"].astype(str)

        # Check if a student with the same name already exists
        if existing_data["Student Name"].str.contains(student_name).any():
            st.warning("A student with this name already exists.")
            st.stop()
        else:
            # Ensure 'Date of Joining' is treated as datetime
            date_of_joining = pd.to_datetime(date_of_joining)

            # Create a new row of student data
            new_data = {
                'AdminNo': [AdminNo],
                'Student Name': [student_name],
                'Grade': [grade],
                'Date of Joining': [date_of_joining],
                'Subject': [subject],
                'Fees': [fees],
                'Amount Paid': [amount_paid],
            }

            new_df = pd.DataFrame(new_data)
            existing_data = pd.concat([existing_data, new_df], ignore_index=True)

            # Save the modified DataFrame back to Google Sheets
            conn.update(data=existing_data, worksheet="Sheet1")

            # Display the updated DataFrame
            st.subheader('Updated Data')
            st.success("Student details successfully submitted!")

            # Convert 'Date of Joining' to string before displaying
            df_display = existing_data.copy()
            df_display['Date of Joining'] = df_display['Date of Joining'].dt.strftime('%Y-%m-%d')

            st.dataframe(df_display)

elif action == "UPDATE EXISTING ENTRY":
    # Display the original data
    st.header('ORIGINAL DATA')
    st.dataframe(existing_data)

    # Display the update form
    st.header('UPDATE EXISTING ENTRY')
    st.markdown("Enter the details to update the existing student entry.")

    # Take input for existing data to be updated
    st.subheader('Enter Existing Data for Update')

    # Use st.form() to wrap the form elements
    with st.form(key='update_form'):
        # Dropdown to select existing student for update
        student_to_update = st.selectbox('Select Student to Update', existing_data['Student Name'])

        # Input fields for update
        updated_grade = st.text_input('Updated Grade')
        updated_date_of_joining = st.date_input('Updated Date of Joining')
        updated_subject = st.text_input('Updated Subject')
        updated_fees = st.number_input('Updated Fees')
        updated_amount_paid = st.number_input('Updated Amount Paid')

        # st.form_submit_button should be used inside the st.form() context
        update_button = st.form_submit_button(label="Update Vendor Details")

    if update_button:
        # Update the DataFrame with the edited data
        existing_data.loc[existing_data['Student Name'] == student_to_update, 'Grade'] = updated_grade
        existing_data.loc[existing_data['Student Name'] == student_to_update, 'Date of Joining'] = pd.to_datetime(
            updated_date_of_joining
        )
        existing_data.loc[existing_data['Student Name'] == student_to_update, 'Subject'] = updated_subject
        existing_data.loc[existing_data['Student Name'] == student_to_update, 'Fees'] = updated_fees
        existing_data.loc[existing_data['Student Name'] == student_to_update, 'Amount Paid'] = updated_amount_paid

        # Save the modified DataFrame back to Google Sheets
        conn.update(data=existing_data, worksheet="Sheet1")

        # Display the updated DataFrame
        st.subheader('Updated Data')
        st.success("Vendor details successfully updated!")

        # Convert 'Date of Joining' to string before displaying
df_display = existing_data.copy()
if 'Date of Joining' in df_display.columns and pd.api.types.is_datetime64_any_dtype(df_display['Date of Joining']):
    df_display['Date of Joining'] = df_display['Date of Joining'].dt.strftime('%Y-%m-%d')


    st.dataframe(df_display)

elif action == "DELETE ENTRY":
    # Display the original data
    st.header('ORIGINAL DATA')
    st.dataframe(existing_data)

    # Display the delete form
    st.header('DELETE ENTRY')
    st.markdown("Enter the details to delete the existing student entry.")

    # Take input for existing data to be deleted
    st.subheader('Enter Existing Data for Deletion')

    # Use st.form() to wrap the form elements
    with st.form(key='delete_form'):
        # Dropdown to select existing student for deletion
        student_to_delete = st.selectbox('Select Student to Delete', existing_data['Student Name'])

        # st.form_submit_button should be used inside the st.form() context
        delete_button = st.form_submit_button(label="Delete Vendor Details")

    if delete_button:
        # Delete the selected row from the DataFrame
        existing_data = existing_data[existing_data['Student Name'] != student_to_delete]

        # Save the modified DataFrame back to Google Sheets
        conn.update(data=existing_data, worksheet="Sheet1")

        # Display the updated DataFrame
        st.subheader('Updated Data')
        st.success("Vendor details successfully deleted!")

        # Convert 'Date of Joining' to string before displaying
df_display = existing_data.copy()
if 'Date of Joining' in df_display.columns and pd.api.types.is_datetime64_any_dtype(df_display['Date of Joining']):
    df_display['Date of Joining'] = df_display['Date of Joining'].dt.strftime('%Y-%m-%d')


elif action == "FEES DUE NEXT MONTH":
    # Display the original data
    st.header('ORIGINAL DATA')
    st.dataframe(existing_data)

    # Display the fees due next month form
    st.header('FEES DUE NEXT MONTH')
    st.markdown("Select students with fees due next month and update the amount paid.")

    # Ensure 'Date of Joining' is treated as datetime
    existing_data['Date of Joining'] = pd.to_datetime(existing_data['Date of Joining'])

    # Get the current month and year
    current_month = pd.to_datetime('today').month
    current_year = pd.to_datetime('today').year

    # Filter students with fees due next month
    due_next_month = (
        existing_data['Date of Joining'].dt.month == current_month
    ) & (existing_data['Date of Joining'].dt.year == current_year)
    students_due_next_month = existing_data[due_next_month]

    # Display the students with fees due next month
    st.subheader('Students with Fees Due Next Month')
    st.dataframe(students_due_next_month)

    # Allow the user to update the amount paid for these students
    st.subheader('Update Amount Paid for Students with Fees Due Next Month')

    # Use st.form() to wrap the form elements
    with st.form(key='fees_due_form'):
        # Multi-select box to choose students to update
        students_to_update = st.multiselect(
            'Select Students to Update', students_due_next_month['Student Name']
        )

        # Input field for updated amount paid
        updated_amount_paid_next_month = st.number_input(
            'Updated Amount Paid for Next Month'
        )

        # st.form_submit_button should be used inside the st.form() context
        update_fees_button = st.form_submit_button(label="Update Fees and Reset for Next Month")

    if update_fees_button:
        # Update the amount paid for selected students
        existing_data.loc[
            existing_data['Student Name'].isin(students_to_update), 'Amount Paid'
        ] = updated_amount_paid_next_month

        # Reset the students for the next month
        existing_data.loc[
            existing_data['Student Name'].isin(students_to_update), 'Date of Joining'
        ] += pd.DateOffset(months=1)

        # Save the modified DataFrame back to Google Sheets
        conn.update(data=existing_data, worksheet="Sheet1")

        # Display the updated DataFrame
        st.subheader('Updated Data')
        st.success("Fees and reset for next month successfully updated!")

        # Convert 'Date of Joining' to string before displaying
        df_display = existing_data.copy()
        df_display['Date of Joining'] = df_display['Date of Joining'].dt.strftime(
            '%Y-%m-%d'
        )

        st.dataframe(df_display)
