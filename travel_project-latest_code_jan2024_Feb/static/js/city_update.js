document.addEventListener("DOMContentLoaded", function () {
    // Add an event listener to the stateselector dropdown for dynamically updating city and category dropdowns
    document.getElementById('stateselector').addEventListener('change', function () {
        var selectedState = this.value;

        // Fetch updated city and category data based on the selected state
        fetch('/get_cities_and_categories/' + selectedState)
            .then(response => response.json())
            .then(data => {
                // Update the city dropdown
                var citySelector = document.getElementById('cityselector');
                citySelector.innerHTML = '';
                data.cities.forEach(function (city) {
                    var option = document.createElement('option');
                    option.value = city;
                    option.text = city;
                    citySelector.appendChild(option);
                });

                // Update the category dropdown
                var categorySelector = document.getElementById('categoryselector');
                categorySelector.innerHTML = '';
                data.categories.forEach(function (category) {
                    var option = document.createElement('option');
                    option.value = category;
                    option.text = category;
                    categorySelector.appendChild(option);
                });
            });
    });

    // Add an event listener to the filterButton
    document.getElementById('filterButton').addEventListener('click', function () {
        // Get the selected values
        var selectedState = document.getElementById('stateselector').value;
        var selectedCity = document.getElementById('cityselector').value;
        var selectedCategory = document.getElementById('categoryselector').value;

        // Fetch updated data based on the selected values
        fetch('/get_filtered_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            });
        });

});    

$(document).ready(function() {
    $('#stateselector').change(function() {
        var selectedState = $(this).val();
        // Make an AJAX request to fetch cities based on selectedState
        $.ajax({
            url: '/get_cities', // Replace with your backend route to fetch cities
            method: 'POST',
            data: { state: selectedState },
            success: function(response) {
                // Clear previous options
                $('#cityselector').empty();
                // Populate with new options
                $.each(response.cities, function(index, city) {
                    $('#cityselector').append($('<option>', {
                        value: city,
                        text: city
                    }));
                });
            }
        });
    });

    // Similarly, you can add change event listeners for other dropdowns and fetch categories
    // $('#cityselector').change(function() { ... });
    // $('#categoryselector').change(function() { ... });
});
