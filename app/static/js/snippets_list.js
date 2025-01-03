$(document).ready(function () {
    var contents = {{ items | safe}};
    function generateContent() {
      $.each(contents, function (index, item) {
        let date = new Date(item.note_update_epoch * 1000)
        let year = date.getFullYear();
        let month = ('0' + (date.getMonth() + 1)).slice(-2);
        let day = ('0' + date.getDate()).slice(-2);
        let hours = ('0' + date.getHours()).slice(-2);
        let minutes = ('0' + date.getMinutes()).slice(-2);
        let formattedDate = year + '-' + month + '-' + day + ' ' + hours + ':' + minutes;
        var $card = $('<div>').addClass('card');
        var $tagsSpan = $('<span>')
          .addClass('editable-text-tags')
          .attr('data-type', 'tags ')
          .attr('data-id', item.note_id)
          .html(item.explore_tag_urls);
        var $urlSpan = $('<span>')
          .addClass('badge badge-default')
          .attr('data-id', item.note_id)
          .html(item.explore_source_url);
        var $contentElement = $('<div>')
          .addClass('editable-text-content')
          .attr('data-type', 'note-content')
          .attr('data-id', item.note_id)
          .html(item.content);
        let $cardBody = $('<div>').addClass('card-body');
        
//        createEditSnippetButton($contentElement, $cardBody, item.id);
        $cardBody.append($('<span>').addClass('badge badge-default').text(formattedDate));
       // $cardBody.append($('<span>').addClass('badge badge-default').html('<a href="' + item.explore_source_url + '">' + item.sources + '</a>'));
        $cardBody.append($urlSpan);
        $cardBody.append($('<br>'));
        $cardBody.append($tagsSpan);
        createEditTagButton($tagsSpan, $cardBody, item.note_id);
        $cardBody.append($('<hr>'));
        $cardBody.append($contentElement);
        createEditContentButton($contentElement, $cardBody, item.note_id);
        $card.append($cardBody);
        $('#content-area').append($card);
        $('#content-area').append($('<br>'));
      });
    }
    function createEditContentButton($elementToEdit, $parentDiv, contentId) {
      var $editButton = $('<button>').addClass('edit-icon').text('Edit Text');
      var $saveButton = $('<button>').addClass('save-icon').text('💾').hide();
      var $inputElement = $('<textarea class="full-width-textarea">');
      $editButton.click(function () {
        var contentRaw = contents.find(item => item.note_id === contentId).content_raw;
        $inputElement.val(contentRaw);
        $elementToEdit.replaceWith($inputElement);
        $inputElement.focus();
        $editButton.hide();
        $saveButton.show();
      });
      $saveButton.click(function () {
        fetch('/update-content', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: contentId,
            content: $inputElement.val(),
          }),
        })
          .then(response => response.json())
          .then(data => {
            fetchUpdatedContent(contentId, $inputElement);
          })
          .catch(error => console.error('Error:', error));
        $saveButton.remove();
        $editButton.remove();
      });
      $parentDiv.append($editButton, $saveButton);
    }
    /*
    function createEditSnippetButton($elementToEdit, $parentDiv, contentId) {
      let $editContentButton = $('<button>').addClass('edit-icon').text('Edit Snippet');
      $editContentButton.click(function () {
       
      });
      $parentDiv.append($editContentButton);
    }
    */

    function fetchUpdatedContent(contentId, $elementToReplace) {
      fetch('/get-updated-content?id=' + contentId)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          var itemIndex = contents.findIndex(item => item.note_id === contentId);
      if (itemIndex !== -1) {
        contents[itemIndex].content = data.content; // Update content_raw if needed
        contents[itemIndex].content_raw = data.content_raw; // Update content_raw if needed
      }
          // Assuming server responds with { content: "new content..." }
          // Create a new element that is non-editable to replace the inputElement
          var $elementToShow = $('<div>')
            .addClass('editable-text-content')
            .attr('data-type', 'note-content')
            .attr('data-id', contentId)
            .html(data.content); 
          $elementToReplace.replaceWith($elementToShow);
          var $parentDiv = $elementToShow.parent();
          


          createEditContentButton($elementToShow, $parentDiv, contentId);


        })
        .catch(error => console.error('Error fetching updated content:', error));
    }

    function fetchUpdatedContent(contentId, $elementToReplace) {
      fetch('/get-updated-content?id=' + contentId)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          var itemIndex = contents.findIndex(item => item.note_id === contentId);
      if (itemIndex !== -1) {
        contents[itemIndex].content = data.content; // Update content_raw if needed
        contents[itemIndex].content_raw = data.content_raw; // Update content_raw if needed
      }
          // Assuming server responds with { content: "new content..." }
          // Create a new element that is non-editable to replace the inputElement
          var $elementToShow = $('<div>')
            .addClass('editable-text-content')
            .attr('data-type', 'note-content')
            .attr('data-id', contentId)
            .html(data.content); 
          $elementToReplace.replaceWith($elementToShow);
          var $parentDiv = $elementToShow.parent();
          


          createEditContentButton($elementToShow, $parentDiv, contentId);


        })
        .catch(error => console.error('Error fetching updated content:', error));
    }
    function createEditTagButton($elementToEdit, $parentDiv, contentId, username) {
      var $editButton = $('<button>').addClass('edit-icon').text('✏️');
      var $saveButton = $('<button>').addClass('save-icon').text('💾').hide();
      var $inputElement;

      $editButton.click(function () {
        // Assume $elementToEdit contains the HTML with tags as links
        // Convert HTML links back to a simple semicolon-separated list of tags for editing
        var tagText = $elementToEdit.find('a').map(function () {
          return $(this).text(); // Extract text from each link
        }).get().join('; '); // Join tags with semicolon and space as delimiter

        $inputElement = $('<input type="text">').val(tagText);
        $elementToEdit.empty().append($inputElement);
        $inputElement.focus();
        $editButton.hide();
        $saveButton.show();
      });

      $saveButton.click(function () {
        var updatedTags = $inputElement.val().split(';').map(function (tag) {
          return tag.trim();
        });
        $elementToEdit.empty(); // Clear the container

        $.each(updatedTags, function (index, tag) {
          if (tag) {
            // Encode tag for URL usage and recreate link HTML
            var encodedTag = encodeURIComponent(tag);
            var linkHtml = $('<a>').attr('href', `/${username}/tag=${encodedTag}`).text(tag);
            $elementToEdit.append(linkHtml);

            if (index < updatedTags.length - 1) {
              $elementToEdit.append('; '); // Add delimiter between tags
            }
          }
        });
        // Switch back to showing the edit button
        $inputElement.remove();
        $saveButton.hide();
        $editButton.show();

        fetch('/update-tags', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: contentId,
            tags: updatedTags,
          }),
        })
          .then(response => response.json())
          .then(data => console.log('Success:', data))
          .catch(error => console.error('Error:', error));
      });


      // Append edit and save buttons next to the tag container
      $parentDiv.append($editButton, $saveButton);
    }
    generateContent();
  }