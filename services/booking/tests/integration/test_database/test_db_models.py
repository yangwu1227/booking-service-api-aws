from datetime import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.db_models import DatabaseOperations
from app.models.pydantic_models import Address, BookingResponse


def test_booking_model(database_session: Session) -> None:
    """
    Test the booking model by saving a new booking request and retrieving it from the database.

    Parameters
    ----------
    database_session : Session
        A SQLAlchemy database session object.
    """
    # Create a new booking request response
    booking_response = BookingResponse(
        id=None,
        event_time=datetime.now(),
        address=Address(
            street="123 Main Street",
            city="Springfield",
            state="IL",
            country="United States",
        ),
        duration_minutes=120,
        topic="Machine Learning",
        requested_by="test@gmail.com",
        status="pending",
    )
    # Database opertaion instance
    db_ops = DatabaseOperations(database_session)

    # Save the record to the database
    db_ops.save_booking(booking_response)
    # Newest record
    new_record = db_ops.list_bookings()[-1]

    # Set the ID of the booking response, since it was originally None, but was auto-generated by the database
    booking_response.id = new_record.id
    assert new_record == booking_response
    assert db_ops.list_booking_by_id(new_record.id) == booking_response

    # Delete the record from the database
    db_ops.delete_booking_by_id(new_record.id)
    # Confirm that the record was deleted, i.e. should raise a 404 error
    with pytest.raises(HTTPException) as exc_info:
        db_ops.list_booking_by_id(new_record.id)
    assert exc_info.value.status_code == 404
