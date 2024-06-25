$(document).ready(function() {
    $('#search').click(function() {
        var query = $('#query').val().trim();
        if (!query.match(/^[a-zA-Z0-9_@. ]+$/)) {
            $('#result-container').html('<p>Invalid search query.</p>');
            return;
        }
        $.ajax({
            url: '/search_user/',
            method: 'GET',
            data: { 'query': query },
            success: function(data) {
                if (data.error) {
                    $('#result-container').html('<p>' + data.error + '</p>');
                } else {
                    // Clear existing iframes and result container
                    $('#result-container').empty();
                    
                    data.forEach(function(user, index) {
                        var iframeId = 'iframe_' + index;
                        var iframeSrc = 'data:text/html;charset=utf-8,' + encodeURIComponent(generateUserHtml(user));
                        var iframeHtml = '<iframe id="' + iframeId + '" class="user-iframe" src="' + iframeSrc + '"></iframe>';
                        
                        // Append iframe to result container
                        $('#result-container').append(iframeHtml);
                        
                        // Store user data in iframe's data attribute for later use
                        $('#' + iframeId).data('user', user);
                    });
                }
            },
            error: function(xhr) {
                $('#result-container').html('<p>Error: ' + xhr.responseText + '</p>');
            }
        });
    });

    // Click handler for iframes to open chat box
    $(document).on('click', '.user-iframe', function() {
        var user = $(this).data('user');
        openChatBox(user);
    });

    // Function to open chat box with selected user
    function openChatBox(user) {
        var chatUrl = 'chat.html?username=' + encodeURIComponent(user.username) +
                      '&name=' + encodeURIComponent(user.name) +
                      '&email=' + encodeURIComponent(user.email);
        window.location.href = chatUrl;
    }

    // Function to generate HTML for user details
    function generateUserHtml(user) {
        var resultHtml = '<p>Username: ' + user.username + '</p>';
        resultHtml += '<p>Name: ' + user.name + '</p>';
        resultHtml += '<p>Email: ' + user.email + '</p>';
        resultHtml += '<p>Relationship Status: ' + user.relationship_status + '</p>';
        resultHtml += '<p>Sexual Orientation: ' + user.sexual_orientation + '</p>';
        resultHtml += '<p>Race: ' + user.race + '</p>';
        resultHtml += '<p>Phone Number: ' + user.phone_number + '</p>';
        resultHtml += '<p>Social Media API: ' + user.social_media_api + '</p>';
        resultHtml += '<p>Birth Date: ' + user.birth_date + '</p>';
        if (user.profile_video) {
            resultHtml += '<p>Profile Video: <a href="' + user.profile_video + '">View</a></p>';
        }
        if (user.location) {
            resultHtml += '<p>Location: ' + user.location + '</p>';
        }
        if (user.tweet) {
            resultHtml += '<p>Tweet: <img src="' + user.tweet + '" alt="Tweet Image"></p>';
        }
        if (user.video) {
            resultHtml += '<p>Video: <a href="' + user.video + '">Watch</a></p>';
        }
        if (user.image) {
            resultHtml += '<p>Image: <img src="' + user.image + '" alt="Profile Image"></p>';
        }
        return resultHtml;
    }
});

