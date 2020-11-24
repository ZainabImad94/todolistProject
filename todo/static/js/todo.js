$(document).ready(function (){
  $("#add_task").click(function () {
        $.ajax({
            url: 'todo/create',
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_form);
            }
        });
    });
    $(".task_edit").click(function () {
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_form);
            }
        })
    });
    $(".task_delete").click(function () {
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_form);
            }
        });
    });

    $('input[name="done"]').click(function () {

        $.ajax({
            url: 'todo/undone/' + $(this).attr('data-id'),
            type: 'get',
            success: function (data) {
                $("#table-task tbody").html(data.html_task_list);
                location.reload();
            }
        })
    });

    $('input[name="undone"]').click(function () {

        $.ajax({
            url: 'todo/done/' + $(this).attr('data-id'),
            type: 'get',
            success: function (data) {
                $("#table-task tbody").html(data.html_task_list);
                location.reload();
            }
        })
    });
    $(".title").click(function () {
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'get',
            dataType: 'json',
        });
    });
    $(".task_view").click(function () {
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html);
            }
        });
    });
    let saveForm = function () {
    let form = $(this);
    $.ajax({
      url: form.attr("action"),
      type: form.attr("method"),
      data: form.serialize(),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
            $("#modal").modal("hide");
            $("#table-task tbody").html(data.html_task_list);  // <-- Replace the table body
            location.reload();
        }
        else {
            $("#modal .modal-content").html(data.html_form);
        }
      },
      error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    return false;
  };
  $("#modal").on("submit", ".js-task-create-form", saveForm);
  $("#modal").on("submit", ".js-task-edit-form", saveForm);
  $("#modal").on("submit", ".js-task-delete-form", saveForm);
});
