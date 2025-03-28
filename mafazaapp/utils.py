from .models import AssignedProject, Transaction, UserLedger
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils.timezone import now
from datetime import timedelta






# def create_transaction(user, project, amount, transaction_type, receipt, narration):
#     print(f"Transaction Debug - Type: {transaction_type}, Amount: {amount}, Project: {project.project_name}")

#     # Get LAST ledger entry FOR THIS SPECIFIC PROJECT
#     last_ledger = UserLedger.objects.filter(
#         transaction__user=user,
        
#         project_name=project.project_name  # Only consider this project's transactions
#     ).order_by('-date').first()
    
#     current_balance = last_ledger.balance if last_ledger else Decimal('0.00')
#     print(f"DEBUG: Current balance for project {project.project_name}: {current_balance}")

#     # Withdrawal logic
#     if transaction_type == 'withdrawal':
#         print("\nDEBUG: Processing WITHDRAWAL")
        
#         if not last_ledger or current_balance < amount:
#             error_msg = f"Insufficient balance in project {project.project_name} for withdrawal. Current balance: {current_balance}"
#             print(f"DEBUG: {error_msg}")
#             raise ValidationError(error_msg)

#         new_balance = current_balance - amount
#         print(f"DEBUG: New balance will be: {new_balance}")

#         transaction = Transaction.objects.create(
#             user=user,
#             project=project,
#             amount=amount,
#             transaction_type='withdrawal',
#             receipt=receipt,  
#             narration=narration,
#         )

#         UserLedger.objects.create(
#             transaction=transaction,
#             date=now(),
#             project_name=project.project_name,
#             principal_investment=Decimal('0.00'),
#             returns=Decimal('0.00'),
#             withdrawal=amount,
#             balance=new_balance,
#             receipt=receipt,
#             narration=narration
#         )

#         print(f"Withdrawal processed. New Balance for {project.project_name}: {new_balance}")
#         return transaction

#     # Investment logic
#     elif transaction_type == 'investment':
#         print("\nDEBUG: Processing INVESTMENT")
        
#         assigned_project = AssignedProject.objects.get(
#             user=user,
#             project=project
#         )
#         roi = assigned_project.rate_of_interest / Decimal('100')
#         annual_return = amount * roi
#         interval_return = (annual_return / Decimal('525600')) * Decimal('2')

#         new_balance = current_balance + interval_return
        
#         print(f"DEBUG: Project ROI: {assigned_project.rate_of_interest}%")
#         print(f"DEBUG: 2-minute return: {interval_return}")
#         print(f"DEBUG: New balance will be: {new_balance}")

#         transaction = Transaction.objects.create(
#             user=user,
#             project=project,
#             amount=amount,
#             transaction_type='investment',
#             status='pending',
#             receipt=receipt,
#             narration=narration,
#         )

#         UserLedger.objects.create(
#             transaction=transaction,
#             date=now(),
#             project_name=project.project_name,
#             principal_investment=amount,
#             returns=interval_return,
#             withdrawal=Decimal('0.00'),
#             balance=new_balance,
#             receipt=receipt,
#             narration=narration
#         )

#         print(f"Investment processed. New Balance for {project.project_name}: {new_balance}")
#         return transaction

# def update_user_ledger(transaction):
#     # Get the last balance from the ledger FOR THIS SPECIFIC PROJECT
#     last_ledger = UserLedger.objects.filter(
#         transaction__user=transaction.user,
#         project_name=transaction.project.project_name
#     ).order_by('-date').first()
    
#     last_balance = last_ledger.balance if last_ledger else Decimal('0.00')
#     print(f"DEBUG: Updating ledger for project {transaction.project.project_name}. Last balance: {last_balance}")

#     if transaction.transaction_type == 'investment':
#         try:
#             assigned_project = AssignedProject.objects.get(
#                 user=transaction.user,
#                 project=transaction.project
#             )
#             roi = assigned_project.rate_of_interest / Decimal('100')
#             annual_return = transaction.amount * roi
#             interval_return = (annual_return / Decimal('525600')) * Decimal('2')

#             new_balance = last_balance + interval_return
#             print(f"DEBUG: Adding {interval_return} to project {transaction.project.project_name}. New balance: {new_balance}")

#             UserLedger.objects.create(
#                 transaction=transaction,
#                 date=now(),
#                 project_name=transaction.project.project_name,
#                 principal_investment=transaction.amount,
#                 returns=interval_return,
#                 withdrawal=Decimal('0.00'),
#                 balance=new_balance,
#             )

#         except AssignedProject.DoesNotExist:
#             raise ValidationError(f"No project assignment found for {transaction.user} in {transaction.project}")

#     elif transaction.transaction_type == 'withdrawal':
#         if last_balance < transaction.amount:
#             raise ValidationError(
#                 f"Insufficient balance in project {transaction.project.project_name}. "
#                 f"Available: {last_balance}, Attempted withdrawal: {transaction.amount}"
#             )
        
#         new_balance = last_balance - transaction.amount
#         print(f"DEBUG: Deducting {transaction.amount} from project {transaction.project.project_name}. New balance: {new_balance}")

#         UserLedger.objects.create(
#             transaction=transaction,
#             date=now(),
#             project_name=transaction.project.project_name,
#             principal_investment=Decimal('0.00'),
#             returns=Decimal('0.00'),
#             withdrawal=transaction.amount,
#             balance=new_balance,
#         )


# from django.core.exceptions import ValidationError
# from django.utils.timezone import now
# from decimal import Decimal



# def generate_missed_returns():
#     transactions = Transaction.objects.filter(transaction_type='investment', status='approved')

#     for transaction in transactions:
#         try:
#             assigned_project = AssignedProject.objects.get(
#                 user=transaction.user,
#                 project=transaction.project
#             )
#         except AssignedProject.DoesNotExist:
#             continue

#         if assigned_project.return_period != '2m':
#             continue

#         # Fetch the latest ledger entry FOR THIS PROJECT
#         last_ledger = UserLedger.objects.filter(
#             transaction__user=transaction.user,
#             project_name=transaction.project.project_name
#         ).order_by('-date').first()
        
#         current_time = now()

#         while last_ledger and last_ledger.date + timedelta(minutes=2) <= current_time:
#             roi = assigned_project.rate_of_interest / Decimal('100')
#             annual_return = transaction.amount * roi
#             interval_return = (annual_return / Decimal('525600')) * Decimal('2')

          
#             last_balance = UserLedger.objects.filter(
#                 transaction__user=transaction.user,
#                 project_name=transaction.project.project_name
#             ).order_by('-date').first().balance

#             new_balance = last_balance + interval_return

#             last_ledger = UserLedger.objects.create(
#                 transaction=transaction,
#                 date=last_ledger.date + timedelta(minutes=2),
#                 project_name=transaction.project.project_name,
#                 principal_investment=Decimal('0.00'),
#                 returns=interval_return,
#                 withdrawal=Decimal('0.00'),
#                 balance=new_balance,
#                 receipt=transaction.receipt
#             )
#             print(f"DEBUG: Added missed return for {transaction.project.project_name}. New balance: {new_balance}")


from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta
from decimal import Decimal

def calculate_interval_return(amount, roi, return_period):
    """
    Calculate returns based on return_period.
    amount: Investment amount (Decimal)
    roi: Rate of Interest (Decimal, e.g., 0.10 for 10%)
    return_period: One of '2m', '10m', 'monthly', etc.
    """
    annual_return = amount * roi
    
    if return_period == '2m':
        return (annual_return / Decimal('525600')) * Decimal('2')  # 2-minute return
    elif return_period == '10m':
        return (annual_return / Decimal('52560')) * Decimal('10')  # 10-minute return
    elif return_period == 'monthly':
        return annual_return / Decimal('12')  # Monthly return
    elif return_period == 'quarterly':
        return annual_return / Decimal('4')  # Quarterly return
    elif return_period == 'semiannual':
        return annual_return / Decimal('2')  # Semiannual return
    elif return_period == 'annual':
        return annual_return  # Annual return
    else:
        raise ValueError(f"Unknown return_period: {return_period}")

def create_transaction(user, project, amount, transaction_type, receipt, narration):
    print(f"Transaction Debug - Type: {transaction_type}, Amount: {amount}, Project: {project.project_name}")

    # Get last ledger entry for this project
    last_ledger = UserLedger.objects.filter(
        transaction__user=user,
        project_name=project.project_name
    ).order_by('-date').first()
    
    current_balance = last_ledger.balance if last_ledger else Decimal('0.00')
    print(f"DEBUG: Current balance for project {project.project_name}: {current_balance}")

    # Withdrawal logic
    if transaction_type == 'withdrawal':
        print("\nDEBUG: Processing WITHDRAWAL")
        
        if not last_ledger or current_balance < amount:
            error_msg = f"Insufficient balance in project {project.project_name} for withdrawal. Current balance: {current_balance}"
            print(f"DEBUG: {error_msg}")
            raise ValidationError(error_msg)

        new_balance = current_balance - amount
        print(f"DEBUG: New balance will be: {new_balance}")

        transaction = Transaction.objects.create(
            user=user,
            project=project,
            amount=amount,
            transaction_type='withdrawal',
            receipt=receipt,
            narration=narration,
        )

        UserLedger.objects.create(
            transaction=transaction,
            date=now(),
            project_name=project.project_name,
            principal_investment=Decimal('0.00'),
            returns=Decimal('0.00'),
            withdrawal=amount,
            balance=new_balance,
            receipt=receipt,
            narration=narration
        )

        print(f"Withdrawal processed. New Balance for {project.project_name}: {new_balance}")
        return transaction

    # Investment logic
    elif transaction_type == 'investment':
        print("\nDEBUG: Processing INVESTMENT")
        
        assigned_project = AssignedProject.objects.get(
            user=user,
            project=project
        )
        
        interval_return = calculate_interval_return(
            amount=amount,
            roi=assigned_project.rate_of_interest / Decimal('100'),
            return_period=assigned_project.return_period
        )

        new_balance = current_balance + interval_return
        
        print(f"DEBUG: Project ROI: {assigned_project.rate_of_interest}%")
        print(f"DEBUG: Calculated return: {interval_return}")
        print(f"DEBUG: New balance will be: {new_balance}")

        transaction = Transaction.objects.create(
            user=user,
            project=project,
            amount=amount,
            transaction_type='investment',
            status='pending',
            receipt=receipt,
            narration=narration,
        )

        UserLedger.objects.create(
            transaction=transaction,
            date=now(),
            project_name=project.project_name,
            principal_investment=amount,
            returns=interval_return,
            withdrawal=Decimal('0.00'),
            balance=new_balance,
            receipt=receipt,
            narration=narration
        )

        print(f"Investment processed. New Balance for {project.project_name}: {new_balance}")
        return transaction

def update_user_ledger(transaction):
    # Get the last balance for this project
    last_ledger = UserLedger.objects.filter(
        transaction__user=transaction.user,
        project_name=transaction.project.project_name
    ).order_by('-date').first()
    
    last_balance = last_ledger.balance if last_ledger else Decimal('0.00')
    print(f"DEBUG: Updating ledger for project {transaction.project.project_name}. Last balance: {last_balance}")

    if transaction.transaction_type == 'investment':
        try:
            assigned_project = AssignedProject.objects.get(
                user=transaction.user,
                project=transaction.project
            )
            
            interval_return = calculate_interval_return(
                amount=transaction.amount,
                roi=assigned_project.rate_of_interest / Decimal('100'),
                return_period=assigned_project.return_period
            )

            new_balance = last_balance + interval_return
            print(f"DEBUG: Adding {interval_return} to project {transaction.project.project_name}. New balance: {new_balance}")

            UserLedger.objects.create(
                transaction=transaction,
                date=now(),
                project_name=transaction.project.project_name,
                principal_investment=transaction.amount,
                returns=interval_return,
                withdrawal=Decimal('0.00'),
                balance=new_balance,
            )

        except AssignedProject.DoesNotExist:
            raise ValidationError(f"No project assignment found for {transaction.user} in {transaction.project}")

    elif transaction.transaction_type == 'withdrawal':
        if last_balance < transaction.amount:
            raise ValidationError(
                f"Insufficient balance in project {transaction.project.project_name}. "
                f"Available: {last_balance}, Attempted withdrawal: {transaction.amount}"
            )
        
        new_balance = last_balance - transaction.amount
        print(f"DEBUG: Deducting {transaction.amount} from project {transaction.project.project_name}. New balance: {new_balance}")

        UserLedger.objects.create(
            transaction=transaction,
            date=now(),
            project_name=transaction.project.project_name,
            principal_investment=Decimal('0.00'),
            returns=Decimal('0.00'),
            withdrawal=transaction.amount,
            balance=new_balance,
        )

def generate_missed_returns():
    transactions = Transaction.objects.filter(transaction_type='investment', status='approved')

    for transaction in transactions:
        try:
            assigned_project = AssignedProject.objects.get(
                user=transaction.user,
                project=transaction.project
            )
        except AssignedProject.DoesNotExist:
            continue

        # Skip if not frequent compounding
        if assigned_project.return_period not in ['2m', '10m']:
            continue

        # Determine interval in minutes
        interval_minutes = 2 if assigned_project.return_period == '2m' else 10
        
        last_ledger = UserLedger.objects.filter(
            transaction__user=transaction.user,
            project_name=transaction.project.project_name
        ).order_by('-date').first()
        
        current_time = now()

        while last_ledger and last_ledger.date + timedelta(minutes=interval_minutes) <= current_time:
            roi = assigned_project.rate_of_interest / Decimal('100')
            interval_return = calculate_interval_return(
                amount=transaction.amount,
                roi=roi,
                return_period=assigned_project.return_period
            )
            
            last_balance = UserLedger.objects.filter(
                transaction__user=transaction.user,
                project_name=transaction.project.project_name
            ).order_by('-date').first().balance

            new_balance = last_balance + interval_return

            last_ledger = UserLedger.objects.create(
                transaction=transaction,
                date=last_ledger.date + timedelta(minutes=interval_minutes),
                project_name=transaction.project.project_name,
                principal_investment=Decimal('0.00'),
                returns=interval_return,
                withdrawal=Decimal('0.00'),
                balance=new_balance,
                receipt=transaction.receipt
            )
            print(f"DEBUG: Added missed return for {transaction.project.project_name}. New balance: {new_balance}")